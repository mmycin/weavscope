"""
WeavScope store — collection and tenant lifecycle.

Responsibilities
----------------
- Ensure the Weaviate collection exists with the correct multi-tenancy
  and vector configuration.
- Create / remove tenants on demand.
- Expose batch insert and query via composed helpers (batch.py / query.py).
"""

from __future__ import annotations

import weaviate
from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.tenants import Tenant
from typing import List, Optional

from weavscope.config.settings import WeaviateConfig
from weavscope.core.connection import get_weaviate_client
from weavscope.core.providers import build_vector_config
from weavscope.utils.logging import get_logger
from weavscope.utils.exceptions import (
    WeavscopeCollectionError,
    WeavscopeTenantError,
)

logger = get_logger(__name__)


class WeavScope:
    """
    High-level entry point for all Weaviate operations.

    Usage (context manager — recommended)
    ------
    config = WeaviateConfig(...)
    with WeavScope(config, ensure_exists=True) as ws:
        ws.ensure_tenant("event-42")
        ws.batch.add_objects("event-42", objects)
        results = ws.query.hybrid("event-42", "user-7", "startup pitch", 10)
        ws.delete_tenant("event-42")

    Manual usage
    ------------
    ws = WeavScope(config)
    try:
        ...
    finally:
        ws.close()
    """

    def __init__(
        self,
        config: WeaviateConfig,
        tenant_id: Optional[str] = None,
    ) -> None:
        """
        Args:
            config:     A WeaviateConfig instance containing connection details.
            tenant_id:  Optional. If provided, WeavScope will ensure this
                        tenant exists on enter and delete it on exit.
        """
        self.config = config
        self.class_name = config.WEAVIATE_CLASS_NAME
        self.tenant_id = tenant_id
        self._client = get_weaviate_client(config)

        # Lazy imports to avoid circular deps
        from weavscope.core.batch import WeavScopeBatch
        from weavscope.core.query import WeavScopeQuery

        self.batch = WeavScopeBatch(self)
        self.query = WeavScopeQuery(self)

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------

    def __enter__(self) -> "WeavScope":
        if self.tenant_id:
            self.ensure_tenant(self.tenant_id)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.tenant_id:
            try:
                self.delete_tenant(self.tenant_id)
            except Exception as exc:
                logger.error(
                    f"Failed to auto-delete tenant '{self.tenant_id}' on scope exit: {exc}"
                )
        self.close()

    def close(self) -> None:
        """Close the underlying Weaviate connection."""
        if self._client:
            self._client.close()
            logger.debug("Weaviate client connection closed.")

    # ------------------------------------------------------------------
    # Collection management
    # ------------------------------------------------------------------

    def ensure_collection(
        self,
        provider: str = "custom",
        model: str = "custom",
        extra_properties: Optional[List[Property]] = None,
    ) -> None:
        """
        Creates the collection if it does not already exist.

        Args:
            provider:          Embedding provider (e.g. "openai", "gemini").
                               Default "custom" (no server-side vectorization).
            model:             Model name for the provider.
            extra_properties:  Additional properties beyond 'tenant_id' and 'object_id'.
        """
        if self._client.collections.exists(self.class_name):
            logger.debug(f"Collection '{self.class_name}' already exists — skipping.")
            return

        vector_cfg = build_vector_config(provider, model)

        base_properties: List[Property] = [
            Property(name="tenant_id", data_type=DataType.TEXT),
            Property(name="object_id", data_type=DataType.TEXT),
        ]
        all_properties = base_properties + (extra_properties or [])

        create_kwargs: dict = dict(
            name=self.class_name,
            multi_tenancy_config=Configure.multi_tenancy(enabled=True),
            properties=all_properties,
        )
        if vector_cfg is not None:
            create_kwargs["vector_config"] = vector_cfg

        try:
            self._client.collections.create(**create_kwargs)
            logger.info(
                f"Created multi-tenant collection '{self.class_name}' "
                f"[provider={provider}, model={model}]."
            )
        except Exception as exc:
            raise WeavscopeCollectionError(
                f"Failed to create collection '{self.class_name}': {exc}"
            ) from exc

    def collection(self):
        """Returns the raw Weaviate collection handle."""
        return self._client.collections.get(self.class_name)

    def delete_collection(self) -> None:
        """
        Permanently deletes the entire collection and ALL tenant data.
        Use with caution — irreversible.
        """
        try:
            self._client.collections.delete(self.class_name)
            logger.warning(
                f"Collection '{self.class_name}' and ALL its tenant data were deleted."
            )
        except Exception as exc:
            raise WeavscopeCollectionError(
                f"Failed to delete collection '{self.class_name}': {exc}"
            ) from exc

    # ------------------------------------------------------------------
    # Tenant management
    # ------------------------------------------------------------------

    def ensure_tenant(self, tenant_id: str) -> None:
        """
        Creates a tenant if it does not already exist (idempotent).

        Args:
            tenant_id: Unique tenant identifier string.
        """
        col = self.collection()
        try:
            col.tenants.create([Tenant(name=tenant_id)])
            logger.info(f"Tenant '{tenant_id}' created in '{self.class_name}'.")
        except Exception as exc:
            if "already exists" in str(exc).lower():
                logger.debug(f"Tenant '{tenant_id}' already exists — skipping.")
            else:
                raise WeavscopeTenantError(
                    f"Failed to create tenant '{tenant_id}': {exc}"
                ) from exc

    def delete_tenant(self, tenant_id: str) -> None:
        """
        Permanently removes a tenant and ALL its data from the collection.

        Args:
            tenant_id: The tenant to remove.

        Raises:
            WeavscopeTenantError: If the deletion fails unexpectedly.
        """
        col = self.collection()
        try:
            col.tenants.remove([tenant_id])
            logger.info(
                f"Tenant '{tenant_id}' and all its data permanently deleted "
                f"from '{self.class_name}'."
            )
        except Exception as exc:
            raise WeavscopeTenantError(
                f"Failed to delete tenant '{tenant_id}': {exc}"
            ) from exc

    def delete_all_tenants(self) -> None:
        """
        Lists every tenant in the collection and removes them all.

        This is the recommended cleanup call at the end of a workflow —
        it wipes all tenant data without dropping the collection schema.
        """
        col = self.collection()
        try:
            existing: dict = col.tenants.get()
            tenant_names = list(existing.keys())
        except Exception as exc:
            raise WeavscopeTenantError(
                f"Failed to list tenants in '{self.class_name}': {exc}"
            ) from exc

        if not tenant_names:
            logger.info(f"No tenants to clean up in '{self.class_name}'.")
            return

        errors: List[str] = []
        for name in tenant_names:
            try:
                col.tenants.remove([name])
                logger.info(f"Deleted tenant '{name}'.")
            except Exception as exc:
                msg = f"Failed to delete tenant '{name}': {exc}"
                logger.error(msg)
                errors.append(msg)

        if errors:
            raise WeavscopeTenantError(
                f"Some tenants could not be deleted:\n" + "\n".join(errors)
            )

        logger.info(
            f"All {len(tenant_names)} tenant(s) cleaned up from '{self.class_name}'."
        )

    def list_tenants(self) -> List[str]:
        """
        Returns a list of all tenant names currently in the collection.

        Returns:
            List of tenant ID strings.
        """
        col = self.collection()
        try:
            existing: dict = col.tenants.get()
            return list(existing.keys())
        except Exception as exc:
            raise WeavscopeTenantError(
                f"Failed to list tenants in '{self.class_name}': {exc}"
            ) from exc