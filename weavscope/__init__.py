"""
WeavScope — a clean, multi-tenant Weaviate wrapper.
"""

from weavscope.core.store import WeavScope
from weavscope.config.settings import WeaviateConfig
from weavscope.utils.exceptions import (
    WeavscopeError,
    WeavscopeConnectionError,
    WeavscopeCollectionError,
    WeavscopeTenantError,
    WeavscopeBatchError,
    WeavscopeQueryError,
)

__all__ = [
    "WeavScope",
    "WeaviateConfig",
    "WeavscopeError",
    "WeavscopeConnectionError",
    "WeavscopeCollectionError",
    "WeavscopeTenantError",
    "WeavscopeBatchError",
    "WeavscopeQueryError",
]
