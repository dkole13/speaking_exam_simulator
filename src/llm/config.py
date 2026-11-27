"""Application configuration based on environment variables and a .env file."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

from core_utils.constants import (
    LLM_MAX_TOKENS,
    LLM_MODEL_FILENAME,
    LLM_MODEL_NAME,
    LLM_N_CTX,
    LLM_TEMPERATURE,
    LLM_TOP_K,
    LLM_TOP_P,
)

load_dotenv()


def _optional_int(name: str):
    """
    Read an optional integer from an environment variable.

    Args:
        name: Name of the environment variable.

    Returns:
        The parsed integer, or None if the variable is unset or contains only whitespace.
    """
    value = os.getenv(name, "").strip()
    return int(value) if value else None


@dataclass(frozen=True)
class Settings:
    """
    Immutable settings for model loading and text generation.

    Attributes:
        model_repo_id: Hugging Face repository ID of the model.
            Environment variable: MODEL_REPO_ID.
        model_filename: Name of the GGUF model file in the repository.
            Environment variable: MODEL_FILENAME.
        n_ctx: Context window size in tokens.
            Environment variable: MODEL_N_CTX.
        n_threads: Number of CPU threads used for inference. None indicates
            that no explicit value is configured.
            Environment variable: MODEL_N_THREADS.
        verbose: Whether verbose logging is enabled. Enabled when the value
            is "true", ignoring case.
            Environment variable: MODEL_VERBOSE.
        temperature: Sampling temperature.
            Environment variable: LLM_TEMPERATURE.
        top_k: Maximum number of highest-probability tokens considered
            during sampling.
            Environment variable: LLM_TOP_K.
        top_p: Cumulative probability threshold for nucleus sampling.
            Environment variable: LLM_TOP_P.
        max_tokens: Maximum number of tokens in the generated response.
            Environment variable: LLM_MAX_TOKENS.
    """

    model_repo_id: str = os.getenv("MODEL_REPO_ID", LLM_MODEL_NAME)
    model_filename: str = os.getenv("MODEL_FILENAME", LLM_MODEL_FILENAME)
    n_ctx: int = int(os.getenv("MODEL_N_CTX", str(LLM_N_CTX)))
    n_threads: int | None = _optional_int("MODEL_N_THREADS")
    verbose: bool = os.getenv("MODEL_VERBOSE", "false").lower() == "true"
    temperature: float = float(os.getenv("LLM_TEMPERATURE", str(LLM_TEMPERATURE)))
    top_k: int = int(os.getenv("LLM_TOP_K", str(LLM_TOP_K)))
    top_p: float = float(os.getenv("LLM_TOP_P", str(LLM_TOP_P)))
    max_tokens: int = int(os.getenv("LLM_MAX_TOKENS", str(LLM_MAX_TOKENS)))


settings = Settings()
