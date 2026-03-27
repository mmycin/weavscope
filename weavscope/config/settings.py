from dataclasses import dataclass
from typing import Final

@dataclass
class WeaviateConfig:
    """
    Configuration settings for connecting to a Weaviate instance
    and specifying embedding model parameters.

    Attributes:
        WEAVIATE_HOST (str): The hostname or IP address of the Weaviate instance.
        WEAVIATE_PORT (int): The HTTP/REST API port of the Weaviate instance.
        WEAVIATE_GRPC_PORT (int): The gRPC port of the Weaviate instance (optional for some advanced features).
        WEAVIATE_API_KEY (str): API key or token used to authenticate with Weaviate.
        WEAVIATE_CLASS_NAME (str): The name of the collection (class) in Weaviate where objects are stored.
        WEAVIATE_EMBEDDING_MODEL_PROVIDER (str): Name of the embedding model provider (e.g., 'openai', 'google').
        WEAVIATE_EMBEDDING_MODEL_NAME (str): Name or identifier of the specific embedding model to use.
        WEAVIATE_EMBEDDING_MODEL_API_KEY (str): API key for the embedding model provider (may differ from Weaviate API key).
    """
    WEAVIATE_HOST: Final[str]
    WEAVIATE_PORT: Final[int]
    WEAVIATE_GRPC_PORT: Final[int]
    WEAVIATE_API_KEY: Final[str]
    WEAVIATE_CLASS_NAME: Final[str]
    WEAVIATE_EMBEDDING_MODEL_PROVIDER: Final[str]
    WEAVIATE_EMBEDDING_MODEL_NAME: Final[str]
    WEAVIATE_EMBEDDING_MODEL_API_KEY: Final[str]