"""Documentation loading and processing for WeavScope knowledge base."""

from pathlib import Path
from typing import Any, Dict


def load_documentation(base_path: Path) -> Dict[str, Any]:
    """Load documentation from LLM.txt and other sources."""
    llm_txt_path = base_path / "LLM.txt"
    readme_path = base_path / "README.md"
    
    docs = {
        "title": "WeavScope Documentation",
        "description": "A clean, multi-tenant wrapper for Weaviate",
        "sections": {}
    }
    
    # Load LLM.txt content
    if llm_txt_path.exists():
        with open(llm_txt_path, 'r', encoding='utf-8') as f:
            llm_content = f.read()
        
        docs["sections"]["technical_reference"] = {
            "title": "Technical Reference",
            "content": llm_content,
            "type": "markdown"
        }
    
    # Load README content
    if readme_path.exists():
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()
        
        docs["sections"]["getting_started"] = {
            "title": "Getting Started",
            "content": readme_content,
            "type": "markdown"
        }
    
    # Add API reference and configuration
    docs["api_reference"] = get_api_reference()
    docs["configuration"] = get_configuration()
    
    return docs


def get_api_reference() -> Dict[str, Any]:
    """Get API reference for WeavScope classes."""
    return {
        "WeavScope": {
            "description": "Main WeavScope class for multi-tenant Weaviate operations",
            "methods": [
                {
                    "name": "__init__",
                    "params": ["config: WeaviateConfig", "tenant_id: str = None"],
                    "description": "Initialize WeavScope with configuration and optional tenant"
                },
                {
                    "name": "ensure_collection",
                    "params": ["provider: str = 'custom'", "model: str = 'custom'", "extra_properties: List[Property] = None"],
                    "description": "Idempotent collection creation"
                },
                {
                    "name": "ensure_tenant",
                    "params": ["tenant_id: str"],
                    "description": "Idempotent tenant creation"
                },
                {
                    "name": "delete_tenant",
                    "params": ["tenant_id: str"],
                    "description": "Delete a specific tenant and its data"
                },
                {
                    "name": "list_tenants",
                    "returns": "List[str]",
                    "description": "Return names of all active tenants"
                }
            ]
        },
        "WeavScopeBatch": {
            "description": "High-level ingestion interface accessed via scope.batch",
            "methods": [
                {
                    "name": "add_objects",
                    "params": ["objects: List[Dict]", "tenant_id: str = None", "id_field: str = None", "vector: List[float] = None"],
                    "description": "Batch insert objects with deterministic UUIDs"
                },
                {
                    "name": "add_object",
                    "params": ["object: Dict", "tenant_id: str = None", "id_field: str = None", "vector: List[float] = None"],
                    "description": "Insert a single object"
                },
                {
                    "name": "delete_objects_where",
                    "params": ["filter_property: str", "filter_value: str", "tenant_id: str = None"],
                    "description": "Delete objects where property equals value"
                }
            ]
        },
        "WeavScopeQuery": {
            "description": "High-level search interface accessed via scope.query",
            "methods": [
                {
                    "name": "hybrid",
                    "params": ["query_text: str", "tenant_id: str = None", "limit: int = 10", "alpha: float = 0.75"],
                    "description": "Hybrid search combining keyword and vector search"
                },
                {
                    "name": "near_text",
                    "params": ["query_text: str", "tenant_id: str = None", "limit: int = 10"],
                    "description": "Semantic search using text embeddings"
                },
                {
                    "name": "near_vector",
                    "params": ["vector: List[float]", "tenant_id: str = None", "limit: int = 10"],
                    "description": "Vector search using pre-computed embeddings"
                },
                {
                    "name": "bm25",
                    "params": ["query_text: str", "tenant_id: str = None", "limit: int = 10"],
                    "description": "Keyword search using BM25 algorithm"
                }
            ]
        }
    }


def get_configuration() -> Dict[str, Any]:
    """Get configuration guide for WeavScope."""
    return {
        "WeaviateConfig": {
            "description": "Configuration dataclass for WeavScope",
            "required_fields": [
                {
                    "name": "WEAVIATE_HOST",
                    "type": "str",
                    "description": "Weaviate hostname (e.g., 'localhost')"
                },
                {
                    "name": "WEAVIATE_CLASS_NAME",
                    "type": "str",
                    "description": "Weaviate collection name (PascalCase)"
                },
                {
                    "name": "WEAVIATE_EMBEDDING_MODEL_PROVIDER",
                    "type": "str",
                    "description": "Provider: openai, azure, cohere, google, gemini, huggingface, voyageai, mistral, jinaai, custom"
                },
                {
                    "name": "WEAVIATE_EMBEDDING_MODEL_NAME",
                    "type": "str",
                    "description": "Model identifier for the provider"
                }
            ],
            "optional_fields": [
                {
                    "name": "WEAVIATE_PORT",
                    "type": "int",
                    "default": 8080,
                    "description": "REST port"
                },
                {
                    "name": "WEAVIATE_GRPC_PORT",
                    "type": "int",
                    "default": 50051,
                    "description": "gRPC port"
                },
                {
                    "name": "WEAVIATE_USE_GRPC",
                    "type": "bool",
                    "default": True,
                    "description": "Use gRPC for batch operations"
                },
                {
                    "name": "WEAVIATE_API_KEY",
                    "type": "str",
                    "default": "",
                    "description": "Weaviate cluster API key"
                },
                {
                    "name": "WEAVIATE_EMBEDDING_MODEL_API_KEY",
                    "type": "str",
                    "default": "",
                    "description": "API key for the embedding provider"
                }
            ]
        }
    }
