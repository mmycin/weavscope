"""
WeaviateConfig — connection and embedding model settings for WeavScope.

Instantiate this with your environment-specific values and pass it to
WeavScope. Configuration is kept in a plain dataclass (no env-var magic)
so the caller fully controls how values are sourced.

Example
-------
import os
from weavscope.config.settings import WeaviateConfig

config = WeaviateConfig(
    WEAVIATE_HOST=os.environ["WEAVIATE_HOST"],
    WEAVIATE_PORT=int(os.environ.get("WEAVIATE_PORT", 8080)),
    WEAVIATE_GRPC_PORT=int(os.environ.get("WEAVIATE_GRPC_PORT", 50051)),
    WEAVIATE_API_KEY=os.environ.get("WEAVIATE_API_KEY", ""),
    WEAVIATE_CLASS_NAME="MyCollection",
    WEAVIATE_EMBEDDING_MODEL_PROVIDER="openai",
    WEAVIATE_EMBEDDING_MODEL_NAME="text-embedding-3-small",
    WEAVIATE_EMBEDDING_MODEL_API_KEY=os.environ["OPENAI_API_KEY"],
)
"""

from dataclasses import dataclass, field
from typing import Final


@dataclass
class WeaviateConfig:
    """
    Configuration settings for connecting to a Weaviate instance
    and specifying embedding model parameters.

    Attributes
    ----------
    WEAVIATE_HOST
        Hostname or IP address of the Weaviate instance.
        Example: "localhost" or "my-weaviate.example.com"

    WEAVIATE_PORT
        HTTP/REST API port. Default: 8080.

    WEAVIATE_GRPC_PORT
        gRPC port (required for batch imports and streaming).
        Default: 50051.

    WEAVIATE_API_KEY
        API key used to authenticate with Weaviate.
        Leave empty ("") for anonymous / open instances.

    WEAVIATE_CLASS_NAME
        Name of the collection (class) in Weaviate.
        Must be a valid GraphQL identifier (PascalCase recommended).
        Example: "Documents", "PitchEmbeddings"

    WEAVIATE_EMBEDDING_MODEL_PROVIDER
        Name of the embedding provider. Supported values:
          openai, azure, cohere, google, gemini,
          huggingface, voyageai, mistral, jinaai, custom
        Use "custom" if you supply vectors yourself at insert time.

    WEAVIATE_EMBEDDING_MODEL_NAME
        Model identifier recognised by the provider.
        Example: "text-embedding-3-small" (OpenAI),
                 "embed-english-v3.0" (Cohere),
                 "models/text-embedding-004" (Gemini)

    WEAVIATE_EMBEDDING_MODEL_API_KEY
        API key for the embedding model provider.
        May be the same as or different from WEAVIATE_API_KEY.
        Leave empty ("") if the provider needs no key.
    """

    WEAVIATE_HOST: str
    WEAVIATE_CLASS_NAME: str
    WEAVIATE_EMBEDDING_MODEL_PROVIDER: str
    WEAVIATE_EMBEDDING_MODEL_NAME: str

    WEAVIATE_PORT: int = 8080
    WEAVIATE_GRPC_PORT: int = 50051
    WEAVIATE_USE_GRPC: bool = True
    WEAVIATE_API_KEY: str = ""
    WEAVIATE_EMBEDDING_MODEL_API_KEY: str = ""

    def __post_init__(self) -> None:
        if not self.WEAVIATE_HOST:
            raise ValueError("WeaviateConfig: WEAVIATE_HOST must not be empty.")
        if not self.WEAVIATE_CLASS_NAME:
            raise ValueError("WeaviateConfig: WEAVIATE_CLASS_NAME must not be empty.")
        if not self.WEAVIATE_EMBEDDING_MODEL_PROVIDER:
            raise ValueError(
                "WeaviateConfig: WEAVIATE_EMBEDDING_MODEL_PROVIDER must not be empty. "
                "Use 'custom' if you supply vectors manually."
            )
        if not self.WEAVIATE_EMBEDDING_MODEL_NAME:
            raise ValueError(
                "WeaviateConfig: WEAVIATE_EMBEDDING_MODEL_NAME must not be empty. "
                "Use 'custom' if you supply vectors manually."
            )
        if self.WEAVIATE_PORT <= 0 or self.WEAVIATE_PORT > 65535:
            raise ValueError(
                f"WeaviateConfig: WEAVIATE_PORT must be 1–65535, got {self.WEAVIATE_PORT}."
            )
        if self.WEAVIATE_GRPC_PORT <= 0 or self.WEAVIATE_GRPC_PORT > 65535:
            raise ValueError(
                f"WeaviateConfig: WEAVIATE_GRPC_PORT must be 1–65535, "
                f"got {self.WEAVIATE_GRPC_PORT}."
            )