"""
WeavScope MCP Integration - Combines WeavScope and Weaviate documentation MCP.

This module integrates the WeaviateDocClient with the WeavScopeKnowledgeBase
to provide a unified documentation interface.
"""

from typing import Dict, Any, Optional
from pathlib import Path
import sys

# Add src to path for absolute imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from client.weaviate_doc_client import WeaviateDocClient
from knowledgebase import WeavScopeKnowledgeBase


class WeavScopeWeaviateIntegration:
    """Integration between WeavScope and Weaviate documentation MCP."""

    def __init__(self):
        """Initialize integration."""
        self.weaviate_client = WeaviateDocClient()
        self.weavscope_kb = WeavScopeKnowledgeBase()

    async def get_integrated_documentation(self) -> Dict[str, Any]:
        """Get integrated WeavScope + Weaviate documentation.

        Returns:
            Combined documentation from both sources.
        """
        weavscope_docs = self.weavscope_kb.get_documentation()
        weaviate_tools = await self.weaviate_client.get_weaviate_tools()

        return {
            "title": "WeavScope + Weaviate Documentation",
            "description": (
                "Complete documentation for WeavScope multi-tenant wrapper "
                "and underlying Weaviate"
            ),
            "weavscope": weavscope_docs,
            "weaviate": {
                "available_tools": weaviate_tools,
                "mcp_url": self.weaviate_client.mcp_url,
                "connection_type": self.weaviate_client.mcp_type,
            },
            "integration_guide": {
                "title": "Integration Guide",
                "content": """
# WeavScope + Weaviate Integration

WeavScope is built on top of Weaviate v4 and provides a simplified multi-tenant interface.
This integrated documentation covers both WeavScope's wrapper functionality and the underlying
Weaviate capabilities.

## Key Integration Points

1. **Multi-tenant Management**: WeavScope handles tenant lifecycle automatically
2. **Simplified API**: WeavScope provides fluent interfaces for common operations
3. **Weaviate Compatibility**: All Weaviate features remain accessible through the client
4. **Configuration**: WeavScope manages Weaviate client configuration and authentication

## When to Use Which

- **Use WeavScope for**: Multi-tenant applications, simplified workflows, automatic cleanup
- **Use Weaviate directly for**: Advanced features, custom configurations, non-multi-tenant use cases
                """,
            },
        }

    async def call_weaviate_tool(
        self, tool_name: str, parameters: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Call a Weaviate documentation tool.

        Args:
            tool_name: Name of the Weaviate tool to call
            parameters: Parameters for the tool call

        Returns:
            Tool response
        """
        return await self.weaviate_client.call_weaviate_tool(tool_name, parameters or {})

    async def close(self):
        """Close the integration."""
        await self.weaviate_client.disconnect()


# ---------------------------------------------------------------------------
# Global integration instance helpers
# ---------------------------------------------------------------------------

_integration: Optional[WeavScopeWeaviateIntegration] = None


async def get_integration() -> WeavScopeWeaviateIntegration:
    """Get or create the global integration instance.

    Returns:
        WeavScopeWeaviateIntegration instance
    """
    global _integration
    if _integration is None:
        _integration = WeavScopeWeaviateIntegration()
        await _integration.weaviate_client.connect()
    return _integration


async def close_integration():
    """Close the global integration instance."""
    global _integration
    if _integration:
        await _integration.close()
        _integration = None
