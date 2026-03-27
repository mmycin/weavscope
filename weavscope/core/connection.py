import threading
import weaviate
from weaviate.classes.init import Auth

from weavscope.config.settings import WeaviateConfig
from weavscope.utils.logging import get_logger
from weavscope.utils.exceptions import WeavscopeConnectionError

logger = get_logger(__name__)

_client_lock = threading.Lock()

_PROVIDER_HEADER_MAP = {
    "openai": "X-OpenAI-Api-Key",
    "cohere": "X-Cohere-Api-Key",
    "google": "X-Goog-Studio-Api-Key",
    "gemini": "X-Goog-Studio-Api-Key",
    "huggingface": "X-HuggingFace-Api-Key",
    "voyageai": "X-VoyageAI-Api-Key",
    "mistral": "X-Mistral-Api-Key",
    "aws": "X-AWS-Access-Key",
    "azure": "X-Azure-Api-Key",
    "jinaai": "X-JinaAI-Api-Key",
}


def _resolve_embedding_header(config: WeaviateConfig) -> dict:
    """Resolves the correct HTTP header(s) for the embedding model provider."""
    provider = (config.WEAVIATE_EMBEDDING_MODEL_PROVIDER or "").lower().strip()
    api_key = config.WEAVIATE_EMBEDDING_MODEL_API_KEY

    if not provider or not api_key:
        return {}

    # For gemini, we send only the Studio-specific headers to avoid
    # triggering Vertex logic or conflicting with Weaviate client auth.
    if provider == "gemini":
        return {
            "X-Goog-Studio-Api-Key": api_key,
            "X-Goog-Api-Key": api_key,
        }

    header_key = _PROVIDER_HEADER_MAP.get(provider)
    if header_key is None:
        logger.warning(
            f"Unknown embedding provider '{provider}'. "
            f"No embedding API header will be sent. "
            f"Known providers: {list(_PROVIDER_HEADER_MAP)}"
        )
        return {}

    return {header_key: api_key}


def get_weaviate_client(config: WeaviateConfig) -> weaviate.WeaviateClient:
    """
    Creates a Weaviate connection from config.
    """
    auth = Auth.api_key(config.WEAVIATE_API_KEY) if config.WEAVIATE_API_KEY else None
    embedding_headers = _resolve_embedding_header(config)

    try:
        with _client_lock:
            # We always pass host/port to satisfy v4 validation,
            # but downstream modules (batch/query) will check USE_GRPC
            # to decide whether to use gRPC-specific methods.
            client = weaviate.connect_to_custom(
                http_host=config.WEAVIATE_HOST,
                http_port=config.WEAVIATE_PORT,
                http_secure=False,
                grpc_host=config.WEAVIATE_HOST,
                grpc_port=config.WEAVIATE_GRPC_PORT,
                grpc_secure=False,
                auth_credentials=auth,
                headers=embedding_headers or None,
                skip_init_checks=True,
            )
        logger.debug(
            f"Weaviate connected (gRPC logic {'enabled' if config.WEAVIATE_USE_GRPC else 'disabled'}) "
            f"-> {config.WEAVIATE_HOST}:{config.WEAVIATE_PORT}"
        )
        return client
    except Exception as exc:
        raise WeavscopeConnectionError(
            f"Failed to connect to Weaviate at "
            f"{config.WEAVIATE_HOST}:{config.WEAVIATE_PORT} - {exc}"
        ) from exc