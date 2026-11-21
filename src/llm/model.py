"""Loader for the local GGUF model."""

from functools import lru_cache
from llama_cpp import Llama

from .config import settings


@lru_cache(maxsize=1)
def get_model() -> Llama:
    """Load the model once per Python process."""
    kwargs = {
        "repo_id": settings.model_repo_id,
        "filename": settings.model_filename,
        "n_ctx": settings.n_ctx,
        "verbose": settings.verbose,
    }
    if settings.n_threads is not None:
        kwargs["n_threads"] = settings.n_threads

    return Llama.from_pretrained(**kwargs)
