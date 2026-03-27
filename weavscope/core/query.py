"""
WeavScope query — semantic and hybrid search within a tenant.

Separated from store.py so callers can import the query surface
independently without carrying the full store overhead.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from weaviate.classes.query import MetadataQuery, Filter

from weavscope.utils.logging import get_logger
from weavscope.utils.exceptions import WeavscopeQueryError

if TYPE_CHECKING:
    from weavscope.core.store import WeavScope

logger = get_logger(__name__)


def _serialize_obj(obj) -> Dict[str, Any]:
    """Converts a Weaviate response object into a plain dict."""
    return {
        "uuid": str(obj.uuid) if obj.uuid else None,
        "properties": obj.properties or {},
        "score": (
            obj.metadata.score
            if obj.metadata and obj.metadata.score is not None
            else None
        ),
        "distance": (
            obj.metadata.distance
            if obj.metadata and obj.metadata.distance is not None
            else None
        ),
        "certainty": (
            obj.metadata.certainty
            if obj.metadata and obj.metadata.certainty is not None
            else None
        ),
    }


class WeavScopeQuery:
    """
    Provides semantic and hybrid search within a tenant.

    Instantiated automatically by WeavScope — do not instantiate directly.
    Access via: ws.query.hybrid(...)
    """

    def __init__(self, store: "WeavScope") -> None:
        self._store = store

    # ------------------------------------------------------------------
    # Hybrid search (BM25 + vector)
    # ------------------------------------------------------------------

    def hybrid(
        self,
        query_text: str,
        tenant_id: Optional[str] = None,
        limit: int = 10,
        alpha: float = 0.75,
        exclude_property: Optional[str] = None,
        exclude_value: Optional[str] = None,
        return_properties: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Runs a hybrid (BM25 + vector) search within a tenant.

        If tenant_id is omitted, it uses the tenant_id defined in the
        WeavScope instance.
        """
        target_tenant = tenant_id or self._store.tenant_id
        if not target_tenant:
            raise WeavscopeQueryError("No tenant_id provided for hybrid search.")

        col = self._store.collection().with_tenant(target_tenant)

        query_kwargs: Dict[str, Any] = dict(
            query=query_text,
            alpha=alpha,
            limit=limit,
            return_metadata=MetadataQuery(score=True, distance=True, certainty=True),
        )

        if exclude_property and exclude_value is not None:
            query_kwargs["filters"] = Filter.by_property(exclude_property).not_equal(
                exclude_value
            )

        if return_properties:
            query_kwargs["return_properties"] = return_properties

        try:
            response = col.query.hybrid(**query_kwargs)
            results = [_serialize_obj(o) for o in response.objects]
            logger.debug(
                f"[query] hybrid '{query_text}' in '{target_tenant}' - {len(results)} results."
            )
            return results
        except Exception as exc:
            raise WeavscopeQueryError(
                f"Hybrid query failed in tenant '{target_tenant}': {exc}"
            ) from exc

    def near_text(
        self,
        query_text: str,
        tenant_id: Optional[str] = None,
        limit: int = 10,
        certainty: Optional[float] = None,
        distance: Optional[float] = None,
        exclude_property: Optional[str] = None,
        exclude_value: Optional[str] = None,
        return_properties: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Runs a pure semantic (near-text) search."""
        target_tenant = tenant_id or self._store.tenant_id
        if not target_tenant:
            raise WeavscopeQueryError("No tenant_id provided for near_text search.")

        col = self._store.collection().with_tenant(target_tenant)

        near_text_kwargs: Dict[str, Any] = {"query": query_text}
        if certainty is not None:
            near_text_kwargs["certainty"] = certainty
        if distance is not None:
            near_text_kwargs["distance"] = distance

        query_kwargs: Dict[str, Any] = dict(
            near_text=near_text_kwargs,
            limit=limit,
            return_metadata=MetadataQuery(score=True, distance=True, certainty=True),
        )

        if exclude_property and exclude_value is not None:
            query_kwargs["filters"] = Filter.by_property(exclude_property).not_equal(
                exclude_value
            )

        if return_properties:
            query_kwargs["return_properties"] = return_properties

        try:
            response = col.query.near_text(**query_kwargs)
            results = [_serialize_obj(o) for o in response.objects]
            logger.debug(
                f"[query] near_text '{query_text}' in '{target_tenant}' - {len(results)} results."
            )
            return results
        except Exception as exc:
            raise WeavscopeQueryError(
                f"near_text query failed in tenant '{target_tenant}': {exc}"
            ) from exc

    def near_vector(
        self,
        vector: List[float],
        tenant_id: Optional[str] = None,
        limit: int = 10,
        certainty: Optional[float] = None,
        distance: Optional[float] = None,
        exclude_property: Optional[str] = None,
        exclude_value: Optional[str] = None,
        return_properties: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Runs a vector search using a pre-computed embedding."""
        target_tenant = tenant_id or self._store.tenant_id
        if not target_tenant:
            raise WeavscopeQueryError("No tenant_id provided for near_vector search.")

        col = self._store.collection().with_tenant(target_tenant)

        near_vec_kwargs: Dict[str, Any] = {"vector": vector}
        if certainty is not None:
            near_vec_kwargs["certainty"] = certainty
        if distance is not None:
            near_vec_kwargs["distance"] = distance

        query_kwargs: Dict[str, Any] = dict(
            near_vector=near_vec_kwargs,
            limit=limit,
            return_metadata=MetadataQuery(score=True, distance=True, certainty=True),
        )

        if exclude_property and exclude_value is not None:
            query_kwargs["filters"] = Filter.by_property(exclude_property).not_equal(
                exclude_value
            )

        if return_properties:
            query_kwargs["return_properties"] = return_properties

        try:
            response = col.query.near_vector(**query_kwargs)
            results = [_serialize_obj(o) for o in response.objects]
            logger.debug(
                f"[query] near_vector in '{target_tenant}' - {len(results)} results."
            )
            return results
        except Exception as exc:
            raise WeavscopeQueryError(
                f"near_vector query failed in tenant '{target_tenant}': {exc}"
            ) from exc

    def bm25(
        self,
        query_text: str,
        tenant_id: Optional[str] = None,
        limit: int = 10,
        properties: Optional[List[str]] = None,
        return_properties: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Runs a BM25 keyword search."""
        target_tenant = tenant_id or self._store.tenant_id
        if not target_tenant:
            raise WeavscopeQueryError("No tenant_id provided for BM25 search.")

        col = self._store.collection().with_tenant(target_tenant)

        query_kwargs: Dict[str, Any] = dict(
            query=query_text,
            limit=limit,
            return_metadata=MetadataQuery(score=True),
        )
        if properties:
            query_kwargs["query_properties"] = properties
        if return_properties:
            query_kwargs["return_properties"] = return_properties

        try:
            response = col.query.bm25(**query_kwargs)
            results = [_serialize_obj(o) for o in response.objects]
            logger.debug(
                f"[query] bm25 '{query_text}' in '{target_tenant}' - {len(results)} results."
            )
            return results
        except Exception as exc:
            raise WeavscopeQueryError(
                f"BM25 query failed in tenant '{target_tenant}': {exc}"
            ) from exc

    def fetch_all(
        self,
        tenant_id: Optional[str] = None,
        limit: int = 100,
        return_properties: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Fetches all objects from a tenant (up to limit)."""
        target_tenant = tenant_id or self._store.tenant_id
        if not target_tenant:
            raise WeavscopeQueryError("No tenant_id provided for fetch_all.")

        col = self._store.collection().with_tenant(target_tenant)

        query_kwargs: Dict[str, Any] = dict(limit=limit)
        if return_properties:
            query_kwargs["return_properties"] = return_properties

        try:
            response = col.query.fetch_objects(**query_kwargs)
            return [_serialize_obj(o) for o in response.objects]
        except Exception as exc:
            raise WeavscopeQueryError(
                f"fetch_all failed in tenant '{target_tenant}': {exc}"
            ) from exc

    def fetch_by_id(
        self,
        uuid: str,
        tenant_id: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Fetches a single object by UUID."""
        target_tenant = tenant_id or self._store.tenant_id
        if not target_tenant:
            raise WeavscopeQueryError("No tenant_id provided for fetch_by_id.")

        col = self._store.collection().with_tenant(target_tenant)
        try:
            obj = col.query.fetch_object_by_id(uuid)
            return _serialize_obj(obj) if obj else None
        except Exception as exc:
            raise WeavscopeQueryError(
                f"fetch_by_id failed in tenant '{target_tenant}': {exc}"
            ) from exc