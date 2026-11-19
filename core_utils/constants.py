from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
MODELS_DIR = PROJECT_ROOT / "models"
ASR_MODEL_NAME = "nvidia/parakeet-tdt-0.6b-v2"
ASR_MODEL_PATH = MODELS_DIR / "parakeet-tdt-0.6b-v2.nemo"
