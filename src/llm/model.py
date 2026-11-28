"""Load and cache the configured GGUF language model."""

import logging
from functools import lru_cache

from llama_cpp import Llama

from .config import settings


logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_model() -> Llama:
    """
    Return the configured Llama language model.

    Returns:
        The initialized Llama model instance.
    """
    logger.info(
        "Loading LLM model: repo_id=%s, filename=%s",
        settings.model_repo_id,
        settings.model_filename,
    )
    kwargs = {
        "repo_id": settings.model_repo_id,
        "filename": settings.model_filename,
        "n_ctx": settings.n_ctx,
        "verbose": settings.verbose,
    }
    if settings.n_threads is not None:
        kwargs["n_threads"] = settings.n_threads

    try:
        model = Llama.from_pretrained(**kwargs)
        logger.info("LLM model loaded successfully.")
        return model

    except Exception:
        logger.exception("Failed to load LLM model.")
        raise
