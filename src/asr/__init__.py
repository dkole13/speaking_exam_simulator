"""Automatic speech recognition (ASR) module.

Turns a recorded user answer into a transcript with word-level timestamps.
Designed to support NVIDIA Parakeet-tdt-0.6b-v2 model.

Public API:
    ASRModule: Class for ASR model inference. Return transcribed text with optional timestamps.
"""

from src.asr.transcript import ASRModule

__all__ = ["ASRModule"]
