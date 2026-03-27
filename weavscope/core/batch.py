"""
WeavScope batch insert — handles object ingestion per tenant.

Separated from store.py so callers can import batch independently
without carrying the full store overhead.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

import weaviate.util

from weavscope.utils.logging import get_logger
from weavscope.utils.uuid import generate_uuid
from weavscope.utils.exceptions import WeavscopeBatchError

if TYPE_CHECKING:
    from weavscope.core.store import WeavScope

logger = get_logger(__name__)


class WeavScopeBatch:
    """
    Handles batch insertion of objects into a specific tenant.

    Instantiated automatically by WeavScope — do not instantiate directly.
    Access via: ws.batch.add_objects(...)
    """

    def __init__(self, store: "WeavScope") -> None:
        self._store = store

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add_objects(
        self,
        objects: List[Dict[str, Any]],
        tenant_id: Optional[str] = None,
        id_field: Optional[str] = None,
        vector: Optional[List[float]] = None,
    ) -> bool:
        """
        Batch-inserts a list of objects into a tenant.

        If tenant_id is omitted, it uses the tenant_id defined in the
        WeavScope instance.

        Args:
            objects:    List of property dicts.
            tenant_id:  Target tenant ID (overrides instance tenant_id).
            id_field:   Optional key inside objects for deterministic UUID.
            vector:     Optional pre-computed vector.

        Returns:
            True on success, False if any objects failed.
        """
        target_tenant = tenant_id or self._store.tenant_id
        if not target_tenant:
            raise WeavscopeBatchError(
                "No tenant_id provided. Either pass tenant_id to add_objects() "
                "or initialize WeavScope with a tenant_id."
            )

        self._store.ensure_tenant(target_tenant)

        if not objects:
            logger.debug(f"[batch] No objects to insert into tenant '{target_tenant}'.")
            return True

        col = self._store.collection().with_tenant(target_tenant)

        # Fallback to REST-only (sequential) insertion if gRPC is disabled
        if not self._store.config.WEAVIATE_USE_GRPC:
            logger.info(
                f"[batch] Using REST-only (sequential) insertion for {len(objects)} "
                f"object(s) into tenant '{target_tenant}'."
            )
            success_count = 0
            try:
                for obj in objects:
                    uuid = (
                        generate_uuid(str(obj.get(id_field, "")), target_tenant)
                        if id_field
                        else None
                    )
                    insert_kwargs: Dict[str, Any] = {"properties": obj}
                    if uuid:
                        insert_kwargs["uuid"] = uuid
                    if vector is not None:
                        insert_kwargs["vector"] = vector
                    
                    col.data.insert(**insert_kwargs)
                    success_count += 1
                return True
            except Exception as exc:
                logger.error(
                    f"[batch] REST insertion failed after {success_count} objects: {exc}"
                )
                return False

        # Standard gRPC-based batching
        try:
            with col.batch.dynamic() as batch:
                for obj in objects:
                    uuid = (
                        generate_uuid(str(obj.get(id_field, "")), target_tenant)
                        if id_field
                        else None
                    )
                    add_kwargs: Dict[str, Any] = {"properties": obj}
                    if uuid:
                        add_kwargs["uuid"] = uuid
                    if vector is not None:
                        add_kwargs["vector"] = vector
                    batch.add_object(**add_kwargs)
        except Exception as exc:
            raise WeavscopeBatchError(
                f"Batch insert failed for tenant '{target_tenant}': {exc}"
            ) from exc

        # Inspect failed objects after the context-manager flush
        failed = col.batch.failed_objects
        if failed:
            for f in failed:
                logger.error(f"[batch] Failed object in '{target_tenant}': {f.message}")
            return False

        logger.info(
            f"[batch] Inserted {len(objects)} object(s) into tenant '{target_tenant}'."
        )
        return True

    def add_object(
        self,
        properties: Dict[str, Any],
        tenant_id: Optional[str] = None,
        id_field: Optional[str] = None,
        vector: Optional[List[float]] = None,
    ) -> bool:
        """Convenience wrapper for a single object."""
        return self.add_objects(
            objects=[properties],
            tenant_id=tenant_id,
            id_field=id_field,
            vector=vector,
        )

    def delete_objects_where(
        self,
        filter_property: str,
        filter_value: str,
        tenant_id: Optional[str] = None,
    ) -> None:
        """Deletes objects matching a filter."""
        target_tenant = tenant_id or self._store.tenant_id
        if not target_tenant:
            raise WeavscopeBatchError("No tenant_id provided for deletion.")

        from weaviate.classes.query import Filter

        col = self._store.collection().with_tenant(target_tenant)
        try:
            col.data.delete_many(
                where=Filter.by_property(filter_property).equal(filter_value)
            )
            logger.info(
                f"[batch] Deleted objects where {filter_property}='{filter_value}' "
                f"in tenant '{target_tenant}'."
            )
        except Exception as exc:
            raise WeavscopeBatchError(
                f"Failed to delete objects in tenant '{target_tenant}': {exc}"
            ) from exc