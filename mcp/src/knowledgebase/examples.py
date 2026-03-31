"""Usage examples for WeavScope knowledge base."""

from typing import List, Dict, Any


def load_examples() -> List[Dict[str, Any]]:
    """Load WeavScope usage examples."""
    return [
        {
            "title": "Basic Usage with Auto-Tenant",
            "description": "Quick start example with automatic tenant management",
            "code": '''from weavscope import WeavScope, WeaviateConfig

config = WeaviateConfig(
    WEAVIATE_HOST="localhost",
    WEAVIATE_PORT=8080,
    WEAVIATE_CLASS_NAME="Articles",
    WEAVIATE_EMBEDDING_MODEL_PROVIDER="gemini",
    WEAVIATE_EMBEDDING_MODEL_NAME="gemini-embedding-001",
    WEAVIATE_EMBEDDING_MODEL_API_KEY="[ENCRYPTION_KEY]"
)

with WeavScope(config, tenant_id="project-A") as scope:
    # Batch-insert objects
    scope.batch.add_objects(
        objects=[
            {"title": "Intro to AI", "content": "AI is changing the world..."},
            {"title": "Vector DBs", "content": "Vector databases are cool."}
        ],
        id_field="title"
    )
    
    # Semantic search
    results = scope.query.hybrid("machine learning")
    for hit in results:
        print(f"Found: {hit['properties']['title']} (score: {hit['score']})")''',
            "language": "python"
        },
        {
            "title": "Manual Tenant Management",
            "description": "Example without automatic tenant deletion",
            "code": '''with WeavScope(config) as scope:
    # Manually ensure a tenant exists
    scope.ensure_tenant("permanent-tenant")
    
    # Add objects to specific tenant
    scope.batch.add_objects(
        tenant_id="permanent-tenant",
        objects=[
            {"title": "Document 1", "content": "Content 1"},
            {"title": "Document 2", "content": "Content 2"}
        ],
        id_field="title"
    )''',
            "language": "python"
        },
        {
            "title": "Advanced Search Queries",
            "description": "Different search methods available",
            "code": '''with WeavScope(config, tenant_id="search-demo") as scope:
    # Hybrid search (default)
    hybrid_results = scope.query.hybrid("machine learning", alpha=0.75)
    
    # Pure semantic search
    semantic_results = scope.query.near_text("artificial intelligence")
    
    # Pure keyword search
    keyword_results = scope.query.bm25("machine learning")
    
    # Vector search with pre-computed embedding
    vector_results = scope.query.near_vector([0.1, 0.2, 0.3, ...])''',
            "language": "python"
        },
        {
            "title": "Configuration Examples",
            "description": "Different provider configurations",
            "code": '''# OpenAI Configuration
openai_config = WeaviateConfig(
    WEAVIATE_HOST="localhost",
    WEAVIATE_CLASS_NAME="Documents",
    WEAVIATE_EMBEDDING_MODEL_PROVIDER="openai",
    WEAVIATE_EMBEDDING_MODEL_NAME="text-embedding-3-small",
    WEAVIATE_EMBEDDING_MODEL_API_KEY="sk-..."
)

# Gemini Configuration
gemini_config = WeaviateConfig(
    WEAVIATE_HOST="localhost",
    WEAVIATE_CLASS_NAME="Documents",
    WEAVIATE_EMBEDDING_MODEL_PROVIDER="gemini",
    WEAVIATE_EMBEDDING_MODEL_NAME="gemini-embedding-001",
    WEAVIATE_EMBEDDING_MODEL_API_KEY="AIza..."
)

# Custom Vectors
custom_config = WeaviateConfig(
    WEAVIATE_HOST="localhost",
    WEAVIATE_CLASS_NAME="Documents",
    WEAVIATE_EMBEDDING_MODEL_PROVIDER="custom",
    WEAVIATE_EMBEDDING_MODEL_NAME="custom"
)''',
            "language": "python"
        }
    ]
