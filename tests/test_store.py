"""
Unit tests for WeavScope (Config-driven).

Using unittest.mock to simulate a live Weaviate instance.
"""

from __future__ import annotations

import pytest
from unittest.mock import MagicMock, patch

from weavscope import (
    WeavScope,
    WeavscopeTenantError,
    WeavscopeBatchError,
    WeavscopeQueryError,
)
from weavscope.config.settings import WeaviateConfig


# ---------------------------------------------------------------------------
# Mock Helpers
# ---------------------------------------------------------------------------

def make_mock_config() -> WeaviateConfig:
    return WeaviateConfig(
        WEAVIATE_HOST="localhost",
        WEAVIATE_CLASS_NAME="TestDocs",
        WEAVIATE_EMBEDDING_MODEL_PROVIDER="openai",
        WEAVIATE_EMBEDDING_MODEL_NAME="text-embedding-3-small",
    )


def make_mock_client(collection_exists: bool = True):
    """Returns a fully mocked weaviate.WeaviateClient."""
    client = MagicMock()
    client.collections.exists.return_value = collection_exists

    # Mock collection handles
    col_mock = MagicMock()
    client.collections.get.return_value = col_mock

    # Mock tenant list
    col_mock.tenants.get.return_value = {
        "tenant-1": MagicMock(name="tenant-1"),
    }

    # Mock with_tenant chain
    col_with_tenant = MagicMock()
    col_mock.with_tenant.return_value = col_with_tenant

    return client, col_mock, col_with_tenant


# ---------------------------------------------------------------------------
# Core Store Tests
# ---------------------------------------------------------------------------

class TestWeavScopeLifecycle:
    @patch("weavscope.core.store.get_weaviate_client")
    def test_init_creates_client(self, mock_get_client):
        client, _, _ = make_mock_client()
        mock_get_client.return_value = client
        
        config = make_mock_config()
        ws = WeavScope(config)
        
        mock_get_client.assert_called_once_with(config)
        assert ws.class_name == "TestDocs"

    @patch("weavscope.core.store.get_weaviate_client")
    def test_enter_exit_lifecycle(self, mock_get_client):
        client, col_mock, _ = make_mock_client()
        mock_get_client.return_value = client
        
        config = make_mock_config()
        with WeavScope(config, tenant_id="t-lifecycle") as ws:
            # Entry: ensure tenant called
            col_mock.tenants.create.assert_called_once()
        
        # Exit: delete tenant and close client
        col_mock.tenants.remove.assert_called_once_with(["t-lifecycle"])
        client.close.assert_called_once()


# ---------------------------------------------------------------------------
# Batch Operations
# ---------------------------------------------------------------------------

class TestBatchOperations:
    @patch("weavscope.core.store.get_weaviate_client")
    def test_add_objects_uses_defaults(self, mock_get_client):
        client, _, col_with_tenant = make_mock_client()
        col_with_tenant.batch.failed_objects = []
        mock_get_client.return_value = client
        
        config = make_mock_config()
        with WeavScope(config, tenant_id="t1") as ws:
            ws.batch.add_objects([{"title": "hi"}])
            
            # Verify the collection was accessed with the correct tenant
            client.collections.get.return_value.with_tenant.assert_called_with("t1")


# ---------------------------------------------------------------------------
# Query Operations
# ---------------------------------------------------------------------------

class TestQueryOperations:
    @patch("weavscope.core.store.get_weaviate_client")
    def test_hybrid_query(self, mock_get_client):
        client, _, col_with_tenant = make_mock_client()
        mock_get_client.return_value = client
        
        # Mock result
        mock_obj = MagicMock()
        mock_obj.uuid = "550e8400-e29b-41d4-a716-446655440000"
        mock_obj.properties = {"text": "found"}
        col_with_tenant.query.hybrid.return_value.objects = [mock_obj]

        config = make_mock_config()
        with WeavScope(config, tenant_id="t1") as ws:
            results = ws.query.hybrid("test")
            assert results[0]["properties"]["text"] == "found"
            col_with_tenant.query.hybrid.assert_called_once()