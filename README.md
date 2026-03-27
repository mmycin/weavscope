# WeavScope 🔭

A clean, multi-tenant wrapper for Weaviate.

WeavScope simplifies working with isolated data in Weaviate by providing a context-managed "Scope" that automatically handles connection, tenant creation, and cleanup based on your configuration.

## Features

- **Config-Driven Lifecycle**: Pass a `WeaviateConfig` object; the wrapper handles the connection.
- **Auto-Tenant Management**: Automatically create a tenant on entry and **DELETES it on exit**.
- **Fluent API**: Simplified batch ingestion and querying (`scope.batch` / `scope.query`).
- **Idempotent Inserts**: Automatic deterministic UUID generation based on `(object_id, tenant_id)`.

## Installation

```bash
pip install weavscope
```

## Quick Start

```python
from weavscope import WeavScope, WeaviateConfig

# 1. Define your connection and class settings
config = WeaviateConfig(
    WEAVIATE_HOST="localhost",  # Your Weaviate host
    WEAVIATE_PORT=8080,
    WEAVIATE_CLASS_NAME="Articles",
    WEAVIATE_EMBEDDING_MODEL_PROVIDER="gemini",
    WEAVIATE_EMBEDDING_MODEL_NAME="gemini-embedding-001",
    WEAVIATE_EMBEDDING_MODEL_API_KEY="[ENCRYPTION_KEY]"
)

# 2. Use WeavScope to isolate operations to a specific tenant
# The tenant 'project-A' is created on entry and DELETED on exit.
with WeavScope(config, tenant_id="project-A") as scope:
    # Batch-insert objects
    scope.batch.add_objects(
        objects=[
            {"title": "Intro to AI", "content": "AI is changing the world..."},
            {"title": "Vector DBs", "content": "Vector databases are cool."}
        ],
        id_field="title"  # Ensures deterministic UUIDs
    )
    
    # Semantic search within the tenant
    results = scope.query.hybrid("machine learning")
    
    for hit in results:
        print(f"Found: {hit['properties']['title']} (score: {hit['score']})")

# Connection is closed and tenant 'project-A' (with all its data) is deleted.
```

## Manual Management

If you don't want the automatic deletion behavior, simply omit the `tenant_id` from the constructor:

```python
with WeavScope(config) as scope:
    # Manually ensure a tenant exists
    scope.ensure_tenant("permanent-tenant")

    # The collection is created automatically if it didn't exist
    scope.batch.add_objects(
        tenant_id="permanent-tenant",
        objects=[...]
    )
```

## License

MIT - Copyright (c) 2026 Tahcin Ul Karim (Mycin)
