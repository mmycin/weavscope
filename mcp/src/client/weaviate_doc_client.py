"""
WeavScope MCP Client - Weaviate Documentation MCP Connection

This module provides a client that connects to the Weaviate documentation MCP server
and exposes its tools and mock responses for use within WeavScope.
"""

from typing import Dict, Any, List
from pathlib import Path
import sys

# Add src to path for absolute imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from client.url import WEAVIATE_MCP_URL, WEAVIATE_MCP_TYPE


class WeaviateDocClient:
    """Client for accessing Weaviate documentation through MCP."""

    def __init__(self, mcp_url: str = WEAVIATE_MCP_URL, mcp_type: str = WEAVIATE_MCP_TYPE):
        """Initialize Weaviate documentation client.

        Args:
            mcp_url: URL of the Weaviate MCP server
            mcp_type: Type of MCP connection (http, websocket, etc.)
        """
        self.mcp_url = mcp_url
        self.mcp_type = mcp_type
        self._connected = False

    async def connect(self) -> bool:
        """Connect to the Weaviate MCP server.

        Returns:
            True if connection successful, False otherwise.
        """
        try:
            # In a real implementation, this would establish MCP connection
            self._connected = True
            return True
        except Exception as e:
            print(f"Failed to connect to Weaviate MCP: {e}")
            return False

    async def disconnect(self):
        """Disconnect from the Weaviate MCP server."""
        self._connected = False

    async def get_weaviate_tools(self) -> List[Dict[str, Any]]:
        """Get list of available Weaviate documentation tools.

        Returns:
            List of available tools with their descriptions.
        """
        if not self._connected:
            await self.connect()

        return [
            {
                "name": "weaviate_get_client_setup",
                "description": "Get Weaviate client setup and configuration guide",
                "parameters": {"type": "object", "properties": {}},
            },
            {
                "name": "weaviate_get_collections",
                "description": "Get Weaviate collections and schema documentation",
                "parameters": {"type": "object", "properties": {}},
            },
            {
                "name": "weaviate_get_query_api",
                "description": "Get Weaviate query API documentation (GraphQL, REST)",
                "parameters": {"type": "object", "properties": {}},
            },
            {
                "name": "weaviate_get_batch_operations",
                "description": "Get Weaviate batch import and operations documentation",
                "parameters": {"type": "object", "properties": {}},
            },
            {
                "name": "weaviate_get_modules",
                "description": "Get Weaviate modules (vectorizers, Q&A, etc.) documentation",
                "parameters": {"type": "object", "properties": {}},
            },
            {
                "name": "weaviate_get_authentication",
                "description": "Get Weaviate authentication and security documentation",
                "parameters": {"type": "object", "properties": {}},
            },
            {
                "name": "weaviate_get_backup_restore",
                "description": "Get Weaviate backup and restore documentation",
                "parameters": {"type": "object", "properties": {}},
            },
            {
                "name": "weaviate_get_troubleshooting",
                "description": "Get Weaviate troubleshooting and common issues",
                "parameters": {"type": "object", "properties": {}},
            },
        ]

    async def call_weaviate_tool(
        self, tool_name: str, parameters: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Call a Weaviate documentation tool.

        Args:
            tool_name: Name of the tool to call
            parameters: Parameters to pass to the tool

        Returns:
            Tool response data
        """
        if not self._connected:
            await self.connect()

        mock_responses = {
            "weaviate_get_client_setup": {
                "title": "Weaviate Client Setup",
                "content": """
# Weaviate Client Setup Guide

## Python Client Installation
```bash
pip install weaviate-client
```

## Basic Client Configuration
```python
import weaviate

# Local Weaviate instance
client = weaviate.Client("http://localhost:8080")

# Cloud instance with API key
client = weaviate.Client(
    url="https://your-cluster.weaviate.network",
    auth_client_secret=weaviate.AuthApiKey(api_key="YOUR_API_KEY")
)
```

## Client with Authentication
```python
# OpenAI API key for vectorization
client = weaviate.Client(
    url="https://your-cluster.weaviate.network",
    auth_client_secret=weaviate.AuthApiKey(api_key="YOUR_API_KEY"),
    additional_config=weaviate.Config(
        additional_headers={
            "X-OpenAI-Api-Key": "YOUR_OPENAI_API_KEY"
        }
    )
)
```
                """,
            },
            "weaviate_get_collections": {
                "title": "Weaviate Collections and Schema",
                "content": """
# Weaviate Collections and Schema

## Define Collection Schema
```python
class_obj = {
    "class": "Article",
    "description": "An article with text content",
    "properties": [
        {
            "name": "title",
            "dataType": ["text"],
            "description": "The title of the article"
        },
        {
            "name": "content",
            "dataType": ["text"],
            "description": "The content of the article"
        },
        {
            "name": "url",
            "dataType": ["text"],
            "description": "URL of the article"
        }
    ],
    "vectorizer": "text2vec-openai"
}

client.schema.create_class(class_obj)
```

## Multi-tenant Collections
```python
multi_tenant_class = {
    "class": "MultiTenantArticle",
    "description": "Multi-tenant article collection",
    "properties": [
        {
            "name": "title",
            "dataType": ["text"]
        },
        {
            "name": "content",
            "dataType": ["text"]
        }
    ],
    "vectorizer": "text2vec-openai",
    "multiTenancyConfig": {
        "enabled": True
    }
}

client.schema.create_class(multi_tenant_class)
```
                """,
            },
            "weaviate_get_query_api": {
                "title": "Weaviate Query API",
                "content": """
# Weaviate Query API

## GraphQL Queries
```python
# Near text search
result = client.query.get("Article", ["title", "content"]) \\
    .with_near_text({"concepts": ["machine learning"]}) \\
    .with_limit(10) \\
    .do()

# Hybrid search
result = client.query.get("Article", ["title", "content"]) \\
    .with_hybrid({"query": "artificial intelligence", "alpha": 0.75}) \\
    .with_limit(10) \\
    .do()

# BM25 keyword search
result = client.query.get("Article", ["title", "content"]) \\
    .with_bm25({"query": "deep learning"}) \\
    .with_limit(10) \\
    .do()
```

## REST API Queries
```python
# Near text search via REST
response = requests.post(
    f"{client_url}/v1/graphql",
    json={
        "query": '''
        {
            Get {
                Article(nearText: {
                    concepts: ["machine learning"],
                    distance: 0.7
                }) {
                    title
                    content
                    _additional {
                        distance
                    }
                }
            }
        }
        '''
    }
)
```
                """,
            },
            "weaviate_get_batch_operations": {
                "title": "Weaviate Batch Operations",
                "content": """
# Weaviate Batch Operations

## Batch Import
```python
# Configure batch client
client.batch.configure(
    batch_size=100,
    dynamic=True,
    timeout_retries=3,
    callback=check_batch_result
)

# Batch import objects
with client.batch as batch:
    for i, data_object in enumerate(data_objects):
        batch.add_data_object(
            data_object=data_object,
            class_name="Article"
        )

        if i % 100 == 0:
            print(f"Imported {i} objects")
```

## Batch with Vectors
```python
with client.batch as batch:
    for i, (data_object, vector) in enumerate(zip(data_objects, vectors)):
        batch.add_data_object(
            data_object=data_object,
            class_name="Article",
            vector=vector
        )
```

## Cross-References in Batch
```python
with client.batch as batch:
    # Add objects with references
    batch.add_data_object(
        data_object={"title": "Main Article"},
        class_name="Article",
        uuid=main_uuid
    )

    batch.add_data_object(
        data_object={"title": "Related Article"},
        class_name="Article",
        uuid=related_uuid,
        references={"refersTo": main_uuid}
    )
```
                """,
            },
            "weaviate_get_modules": {
                "title": "Weaviate Modules",
                "content": """
# Weaviate Modules

## Vectorizer Modules
- **text2vec-openai**: OpenAI embeddings
- **text2vec-cohere**: Cohere embeddings
- **text2vec-huggingface**: Hugging Face model embeddings
- **text2vec-palm**: Google PaLM embeddings
- **text2vec-contextionary**: Weaviate's built-in module

## Q&A Modules
- **qna-openai**: OpenAI question answering
- **qna-cohere**: Cohere question answering

## Generative Modules
- **generative-openai**: OpenAI text generation
- **generative-cohere**: Cohere text generation

## Module Configuration
```python
# OpenAI vectorizer configuration
class_obj = {
    "class": "Document",
    "properties": [
        {"name": "content", "dataType": ["text"]}
    ],
    "vectorizer": "text2vec-openai",
    "moduleConfig": {
        "text2vec-openai": {
            "model": "text-embedding-ada-002",
            "type": "text"
        }
    }
}
```
                """,
            },
            "weaviate_get_authentication": {
                "title": "Weaviate Authentication",
                "content": """
# Weaviate Authentication

## API Key Authentication
```python
import weaviate

client = weaviate.Client(
    url="https://your-cluster.weaviate.network",
    auth_client_secret=weaviate.AuthApiKey(api_key="YOUR_API_KEY")
)
```

## OIDC Authentication
```python
client = weaviate.Client(
    url="https://your-cluster.weaviate.network",
    auth_client_secret=weaviate.AuthBearerToken(
        access_token="YOUR_ACCESS_TOKEN",
        expires_in_seconds=3600
    )
)
```

## Client Credentials
```python
credentials = weaviate.auth.AuthClientPassword(
    username="your-username",
    password="your-password"
)

client = weaviate.Client(
    url="https://your-cluster.weaviate.network",
    auth_client_secret=credentials
)
```
                """,
            },
            "weaviate_get_backup_restore": {
                "title": "Weaviate Backup and Restore",
                "content": """
# Weaviate Backup and Restore

## Create Backup
```python
# Backup to local filesystem
client.backup.create(
    backup_id="my-backup",
    backend="filesystem",
    wait_for_completion=True
)

# Backup to S3
client.backup.create(
    backup_id="my-s3-backup",
    backend="s3",
    config={
        "bucket": "my-backup-bucket",
        "endpoint": "s3.amazonaws.com"
    }
)
```

## Restore Backup
```python
# Restore from local filesystem
client.backup.restore(
    backup_id="my-backup",
    backend="filesystem",
    wait_for_completion=True
)

# Restore from S3
client.backup.restore(
    backup_id="my-s3-backup",
    backend="s3",
    config={
        "bucket": "my-backup-bucket",
        "endpoint": "s3.amazonaws.com"
    }
)
```
                """,
            },
            "weaviate_get_troubleshooting": {
                "title": "Weaviate Troubleshooting",
                "content": """
# Weaviate Troubleshooting

## Common Issues

### Connection Issues
```python
# Check connection status
client.is_ready()  # Returns True if Weaviate is ready

# Get cluster status
client.is_live()   # Returns True if cluster is live
```

### Schema Validation Errors
- Check property data types match schema
- Verify vectorizer configuration
- Ensure class names are properly formatted

### Memory Issues
- Increase batch size for large imports
- Use dynamic batching for variable object sizes
- Monitor memory usage during imports

### Performance Optimization
- Use appropriate vectorizer models
- Optimize batch sizes (typically 100-1000)
- Consider using gRPC for better performance
                """,
            },
        }

        return mock_responses.get(tool_name, {"error": f"Tool {tool_name} not found"})
