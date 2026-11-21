from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
MODELS_DIR = PROJECT_ROOT / "models"
ASR_MODEL_NAME = "nvidia/parakeet-tdt-0.6b-v2"
ASR_MODEL_PATH = MODELS_DIR / "parakeet-tdt-0.6b-v2.nemo"
VAD_THRESHOLD = 0.2  # pause duration in seconds. 0.2s is optimal for non-native english speakers in spontaneous speech
DB_PATH = PROJECT_ROOT / "task_corpus" / "audio_files.db"
CORPUS_DIR = PROJECT_ROOT / "task_corpus"
AUDIO_EXTENSIONS = [".wav"]
