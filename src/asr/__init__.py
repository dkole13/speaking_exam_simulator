"""Automatic speech recognition (ASR) module.

Turns a recorded user answer into a transcript with word-level timestamps.
Designed to support NVIDIA Parakeet-tdt-0.6b-v2 model.

Public API:
    ASRModule: Class for ASR model inference. Return transcribed text with optional timestamps.
    count_wer: Function for counting WER.
"""

from src.asr.pauses import get_pauses
from src.asr.transcript import ASRModule
from src.asr.wer import count_wer

__all__ = ["ASRModule", "count_wer", "get_pauses"]
