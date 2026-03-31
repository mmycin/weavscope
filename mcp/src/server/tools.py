"""MCP server tools - WeavScope documentation and knowledge base."""

import asyncio
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict, List
from fastmcp import FastMCP

# Add src to path for absolute imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import knowledge base
from knowledgebase import WeavScopeKnowledgeBase
from knowledgebase.installation import get_installation_guide, get_quick_install, get_requirements
from client.integration import get_integration, close_integration

# Create MCP instance for decorators
mcp = FastMCP("weavscope-docs", stateless_http=True)

# Initialize knowledge base
kb = WeavScopeKnowledgeBase()

# ============================================================================
# WeavScope Documentation Tools
# ============================================================================

@mcp.tool
def get_weavscope_documentation() -> Dict[str, Any]:
    """Get comprehensive WeavScope documentation.

    Returns:
        Complete WeavScope documentation including API reference, configuration, and examples.
    """
    return kb.get_documentation()

@mcp.tool
def get_weavscope_examples() -> List[Dict[str, Any]]:
    """Get WeavScope usage examples.

    Returns:
        List of code examples demonstrating WeavScope functionality.
    """
    return kb.get_examples()

@mcp.tool
def get_api_reference() -> Dict[str, Any]:
    """Get WeavScope API reference.

    Returns:
        Detailed API reference for all WeavScope classes and methods.
    """
    return kb.get_api_reference()

@mcp.tool
def get_configuration_guide() -> Dict[str, Any]:
    """Get WeavScope configuration guide.

    Returns:
        Configuration guide for different providers and settings.
    """
    return kb.get_configuration_guide()

@mcp.tool
def get_installation_guide() -> Dict[str, Any]:
    """Get comprehensive WeavScope installation guide.

    Returns:
        Complete installation instructions including all methods and requirements.
    """
    return get_installation_guide()

@mcp.tool
def get_quick_install() -> Dict[str, Any]:
    """Get quick installation commands for WeavScope.

    Returns:
        Most common installation methods for quick setup.
    """
    return get_quick_install()

@mcp.tool
def get_requirements() -> Dict[str, Any]:
    """Get detailed requirements for WeavScope.

    Returns:
        System requirements and dependencies for all providers.
    """
    return get_requirements()

# ============================================================================
# Weaviate Documentation Integration Tools
# ============================================================================

@mcp.tool
async def get_integrated_documentation() -> Dict[str, Any]:
    """Get integrated WeavScope + Weaviate documentation.

    Returns:
        Combined documentation from WeavScope and Weaviate MCP servers.
    """
    integration = await get_integration()
    return await integration.get_integrated_documentation()

@mcp.tool
async def get_weaviate_tools() -> List[Dict[str, Any]]:
    """Get available Weaviate documentation tools.

    Returns:
        List of available Weaviate MCP tools with descriptions.
    """
    integration = await get_integration()
    return await integration.weaviate_client.get_weaviate_tools()

@mcp.tool
async def call_weaviate_tool(tool_name: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
    """Call a Weaviate documentation tool.

    Args:
        tool_name: Name of the Weaviate tool to call
        parameters: Optional parameters for the tool call

    Returns:
        Response from the Weaviate documentation tool.
    """
    integration = await get_integration()
    return await integration.call_weaviate_tool(tool_name, parameters)

@mcp.tool
async def get_weaviate_client_setup() -> Dict[str, Any]:
    """Get Weaviate client setup and configuration guide.

    Returns:
        Weaviate client setup documentation.
    """
    integration = await get_integration()
    return await integration.call_weaviate_tool("weaviate_get_client_setup")

@mcp.tool
async def get_weaviate_collections() -> Dict[str, Any]:
    """Get Weaviate collections and schema documentation.

    Returns:
        Weaviate collections and schema documentation.
    """
    integration = await get_integration()
    return await integration.call_weaviate_tool("weaviate_get_collections")

@mcp.tool
async def get_weaviate_query_api() -> Dict[str, Any]:
    """Get Weaviate query API documentation (GraphQL, REST).

    Returns:
        Weaviate query API documentation.
    """
    integration = await get_integration()
    return await integration.call_weaviate_tool("weaviate_get_query_api")

@mcp.tool
async def get_weaviate_batch_operations() -> Dict[str, Any]:
    """Get Weaviate batch import and operations documentation.

    Returns:
        Weaviate batch operations documentation.
    """
    integration = await get_integration()
    return await integration.call_weaviate_tool("weaviate_get_batch_operations")

@mcp.tool
async def get_weaviate_modules() -> Dict[str, Any]:
    """Get Weaviate modules (vectorizers, Q&A, etc.) documentation.

    Returns:
        Weaviate modules documentation.
    """
    integration = await get_integration()
    return await integration.call_weaviate_tool("weaviate_get_modules")

@mcp.tool
async def get_weaviate_authentication() -> Dict[str, Any]:
    """Get Weaviate authentication and security documentation.

    Returns:
        Weaviate authentication documentation.
    """
    integration = await get_integration()
    return await integration.call_weaviate_tool("weaviate_get_authentication")

@mcp.tool
async def get_weaviate_backup_restore() -> Dict[str, Any]:
    """Get Weaviate backup and restore documentation.

    Returns:
        Weaviate backup and restore documentation.
    """
    integration = await get_integration()
    return await integration.call_weaviate_tool("weaviate_get_backup_restore")

@mcp.tool
async def get_weaviate_troubleshooting() -> Dict[str, Any]:
    """Get Weaviate troubleshooting and common issues.

    Returns:
        Weaviate troubleshooting documentation.
    """
    integration = await get_integration()
    return await integration.call_weaviate_tool("weaviate_get_troubleshooting")

@mcp.resource("weavscope://docs/overview")
def get_overview() -> str:
    """WeavScope overview documentation."""
    docs = kb.get_documentation()
    return f"# {docs['title']}\n\n{docs['description']}"

@mcp.resource("weavscope://docs/getting-started")
def get_getting_started() -> str:
    """WeavScope getting started guide."""
    docs = kb.get_documentation()
    section = docs["sections"].get("getting_started", {})
    return section.get("content", "# Getting Started\n\nDocumentation not available.")

@mcp.resource("weavscope://docs/technical-reference")
def get_technical_reference() -> str:
    """WeavScope technical reference."""
    docs = kb.get_documentation()
    section = docs["sections"].get("technical_reference", {})
    return section.get("content", "# Technical Reference\n\nDocumentation not available.")

@mcp.resource("weavscope://examples/basic-usage")
def get_basic_usage_example() -> str:
    """Basic WeavScope usage example."""
    examples = kb.get_examples()
    if examples:
        example = examples[0]
        return f"# {example['title']}\n\n{example['description']}\n\n```python\n{example['code']}\n```"
    return "# Basic Usage\n\nExample not available."

@mcp.resource("weavscope://examples/advanced-search")
def get_advanced_search_example() -> str:
    """Advanced search examples."""
    examples = kb.get_examples()
    for example in examples:
        if "Advanced Search" in example["title"]:
            return f"# {example['title']}\n\n{example['description']}\n\n```python\n{example['code']}\n```"
    return "# Advanced Search\n\nExample not available."

# ============================================================================
# Weaviate Documentation Resources
# ============================================================================

@mcp.resource("weavscope://weaviate/client-setup")
async def get_weaviate_client_setup_resource() -> str:
    """Weaviate client setup documentation."""
    integration = await get_integration()
    result = await integration.call_weaviate_tool("weaviate_get_client_setup")
    return result.get("content", "# Weaviate Client Setup\n\nDocumentation not available.")

@mcp.resource("weavscope://weaviate/collections")
async def get_weaviate_collections_resource() -> str:
    """Weaviate collections and schema documentation."""
    integration = await get_integration()
    result = await integration.call_weaviate_tool("weaviate_get_collections")
    return result.get("content", "# Weaviate Collections\n\nDocumentation not available.")

@mcp.resource("weavscope://weaviate/query-api")
async def get_weaviate_query_api_resource() -> str:
    """Weaviate query API documentation."""
    integration = await get_integration()
    result = await integration.call_weaviate_tool("weaviate_get_query_api")
    return result.get("content", "# Weaviate Query API\n\nDocumentation not available.")

@mcp.resource("weavscope://weaviate/batch-operations")
async def get_weaviate_batch_operations_resource() -> str:
    """Weaviate batch operations documentation."""
    integration = await get_integration()
    result = await integration.call_weaviate_tool("weaviate_get_batch_operations")
    return result.get("content", "# Weaviate Batch Operations\n\nDocumentation not available.")

@mcp.resource("weavscope://weaviate/modules")
async def get_weaviate_modules_resource() -> str:
    """Weaviate modules documentation."""
    integration = await get_integration()
    result = await integration.call_weaviate_tool("weaviate_get_modules")
    return result.get("content", "# Weaviate Modules\n\nDocumentation not available.")

@mcp.resource("weavscope://weaviate/authentication")
async def get_weaviate_authentication_resource() -> str:
    """Weaviate authentication documentation."""
    integration = await get_integration()
    result = await integration.call_weaviate_tool("weaviate_get_authentication")
    return result.get("content", "# Weaviate Authentication\n\nDocumentation not available.")

@mcp.resource("weavscope://weaviate/backup-restore")
async def get_weaviate_backup_restore_resource() -> str:
    """Weaviate backup and restore documentation."""
    integration = await get_integration()
    result = await integration.call_weaviate_tool("weaviate_get_backup_restore")
    return result.get("content", "# Weaviate Backup and Restore\n\nDocumentation not available.")

@mcp.resource("weavscope://weaviate/troubleshooting")
async def get_weaviate_troubleshooting_resource() -> str:
    """Weaviate troubleshooting documentation."""
    integration = await get_integration()
    result = await integration.call_weaviate_tool("weaviate_get_troubleshooting")
    return result.get("content", "# Weaviate Troubleshooting\n\nDocumentation not available.")
