"""
Resolves the correct Weaviate vector configuration for each supported
embedding provider. Add new providers here — the rest of the codebase
picks them up automatically via build_vector_config().
"""

from weaviate.classes.config import Configure
from weavscope.utils.exceptions import WeavscopeConfigError


def build_vector_config(provider: str, model: str):
    """
    Returns the appropriate Weaviate vector configuration object for a given
    embedding provider and model name.

    Supported providers
    -------------------
    openai      → text2vec_openai
    azure       → text2vec_azure_openai  (model = deployment name)
    cohere      → text2vec_cohere
    google      → text2vec_palm          (legacy Vertex AI)
    gemini      → text2vec_google_gemini (Gemini API)
    huggingface → text2vec_huggingface
    voyageai    → text2vec_voyageai
    mistral     → text2vec_mistral
    jinaai      → text2vec_jinaai
    custom      → No provider-side vectoriser; embeddings must be
                  supplied by the caller at insert time.

    Args:
        provider: Lower-cased provider name (e.g. "openai", "gemini").
        model:    The model identifier recognised by that provider.

    Returns:
        A Weaviate VectorConfig object.

    Raises:
        WeavscopeConfigError: If the provider name is not recognised.
    """
    p = provider.lower().strip()

    if p == "openai":
        return Configure.Vectors.text2vec_openai(model=model)

    if p in ("google", "vertexai"):
        # Legacy Palm / Vertex AI integration
        return Configure.Vectors.text2vec_palm(model_id=model)

    if p == "gemini":
        return Configure.Vectors.text2vec_google_gemini(
            model=model,
            task_type="RETRIEVAL_QUERY",
        )

    if p == "cohere":
        return Configure.Vectors.text2vec_cohere(model=model)

    if p == "huggingface":
        return Configure.Vectors.text2vec_huggingface(model=model)

    if p == "voyageai":
        return Configure.Vectors.text2vec_voyageai(model=model)

    if p == "mistral":
        return Configure.Vectors.text2vec_mistral(model=model)

    if p == "jinaai":
        return Configure.Vectors.text2vec_jinaai(model=model)

    if p == "azure":
        # 'model' is treated as the Azure deployment name
        return Configure.Vectors.text2vec_azure_openai(deployment_id=model)

    if p == "custom":
        # No server-side vectoriser — caller supplies vectors via `vector=` on insert
        return None

    raise WeavscopeConfigError(
        f"Unknown embedding provider '{provider}'. "
        f"Supported: openai, azure, cohere, google, gemini, "
        f"huggingface, voyageai, mistral, jinaai, custom."
    )