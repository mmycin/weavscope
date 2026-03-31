"""
WeavScope MCP Client - Public API

Re-exports all public symbols for backward compatibility.
Import from the specific sub-modules for new code:
  - client.weaviate_doc_client -> WeaviateDocClient
  - client.integration        -> WeavScopeWeaviateIntegration,
                                  get_integration, close_integration
"""

from client.weaviate_doc_client import WeaviateDocClient
from client.integration import (
    WeavScopeWeaviateIntegration,
    get_integration,
    close_integration,
)

__all__ = [
    "WeaviateDocClient",
    "WeavScopeWeaviateIntegration",
    "get_integration",
    "close_integration",
]