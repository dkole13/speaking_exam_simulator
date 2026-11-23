from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
MODELS_DIR = PROJECT_ROOT / "models"
CORPUS_DIR = PROJECT_ROOT / "task_corpus"
ANSWERS_DIR = PROJECT_ROOT / "user_answers"

ASR_MODEL_NAME = "nvidia/parakeet-tdt-0.6b-v2"
ASR_MODEL_PATH = MODELS_DIR / "parakeet-tdt-0.6b-v2.nemo"
VAD_THRESHOLD = 0.2  # pause duration in seconds. 0.2s is optimal for non-native english speakers in spontaneous speech

DB_PATH = PROJECT_ROOT / "task_corpus" / "audio_files.db"
AUDIO_EXTENSIONS = [".wav"]

LLM_MODEL_NAME = "LiquidAI/LFM2.5-1.2B-Instruct-GGUF"
LLM_MODEL_FILENAME = "LFM2.5-1.2B-Instruct-Q4_K_M.gguf"
LLM_N_CTX = 4096
LLM_MAX_TOKENS = 1024
LLM_TEMPERATURE = 0.8
LLM_TOP_K = 50
LLM_TOP_P = 1
REPETITION = "repetition"
INTERVIEW = "interview"
SUPPORTED_TASK_TYPES = (REPETITION, INTERVIEW)
ANSWERS_PER_TASK = {
    REPETITION: 7,
    INTERVIEW: 4,
}
MIN_ANSWER_SCORE = 0
MAX_ANSWER_SCORE = 5
MAX_TASK_SCORE = {
    REPETITION: 35,
    INTERVIEW: 20,
}

