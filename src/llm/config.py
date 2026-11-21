"""Environment-based configuration."""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


def _optional_int(name: str):
    value = os.getenv(name, "").strip()
    return int(value) if value else None


@dataclass(frozen=True)
class Settings:
    model_repo_id: str = os.getenv("MODEL_REPO_ID", "LiquidAI/LFM2.5-1.2B-Instruct-GGUF")
    model_filename: str = os.getenv("MODEL_FILENAME", "LFM2.5-1.2B-Instruct-Q4_K_M.gguf")
    n_ctx: int = int(os.getenv("MODEL_N_CTX", "4096"))
    n_threads: int | None = _optional_int("MODEL_N_THREADS")
    verbose: bool = os.getenv("MODEL_VERBOSE", "false").lower() == "true"
    temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.2"))
    top_p: float = float(os.getenv("LLM_TOP_P", "0.8"))
    max_tokens: int = int(os.getenv("LLM_MAX_TOKENS", "900"))


settings = Settings()
