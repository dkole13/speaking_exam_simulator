from pathlib import Path
from typing import Final

PROJECT_ROOT = Path(__file__).parent.parent
MODELS_DIR = PROJECT_ROOT / "models"
ASR_MODEL_NAME = "nvidia/parakeet-tdt-0.6b-v2"
ASR_MODEL_PATH = MODELS_DIR / "parakeet-tdt-0.6b-v2.nemo"
VAD_THRESHOLD = 0.2  # pause duration in seconds. 0.2s is optimal for non-native english speakers in spontaneous speech
DB_PATH = PROJECT_ROOT / "task_corpus" / "audio_files.db"
CORPUS_DIR = PROJECT_ROOT / "task_corpus"
AUDIO_EXTENSIONS = [".wav"]
LLM_MODEL_NAME: Final[str] = "LiquidAI/LFM2.5-1.2B-Instruct-GGUF"
LLM_MODEL_FILENAME: Final[str] = "LFM2.5-1.2B-Instruct-Q4_K_M.gguf"
LLM_N_CTX: Final[int] = 4096
LLM_MAX_TOKENS: Final[int] = 1024
LLM_TEMPERATURE: Final[float] = 0.8
LLM_TOP_K: Final[int] = 50
LLM_TOP_P: Final[float] = 1
REPETITION: Final[str] = "repetition"
INTERVIEW: Final[str] = "interview"
SUPPORTED_TASK_TYPES: Final[tuple[str, ...]] = (REPETITION, INTERVIEW)
ANSWERS_PER_TASK: Final[dict[str, int]] = {
    REPETITION: 7,
    INTERVIEW: 4,
}
MIN_ANSWER_SCORE: Final[int] = 0
MAX_ANSWER_SCORE: Final[int] = 5
MAX_TASK_SCORE: Final[dict[str, int]] = {
    REPETITION: 35,
    INTERVIEW: 20,
}

