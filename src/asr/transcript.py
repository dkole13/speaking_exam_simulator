import logging
from pathlib import Path

import nemo.collections.asr as nemo_asr

from core_utils.constants import ASR_MODEL_NAME, ASR_MODEL_PATH
from core_utils.timestamps import ASRTimestampsTypes

logger = logging.getLogger(__name__)


class ASRModule:
    """Class for ASR model inference. Designed to work with nvidia/parakeet-tdt-0.6b-v2."""

    def __init__(self):
        """Initialize class instance."""
        self._model_name = ASR_MODEL_NAME
        self._model_path = ASR_MODEL_PATH
        self._model = self._init_model()

    def _init_model(self):
        """Initialize ASR model."""
        if self._model_path.exists():
            logger.info(f"Loading model from {self._model_path}.")
            return nemo_asr.models.ASRModel.restore_from(restore_path=self._model_path)
        else:
            logger.info("Downloading ASR model.")
            return nemo_asr.models.ASRModel.from_pretrained(model_name=self._model_name)

    def _infer(self, audio_path: Path | str, put_timestamps=True):
        """
        Infer ASR model.

        Args:
            audio_path: Path to audio file.
            put_timestamps: Specify the need for timestamps.
        """
        if isinstance(audio_path, Path):
            audio_path = str(audio_path)

        transcript = self._model.transcribe([audio_path], timestamps=put_timestamps, verbose=False)
        return transcript[0]

    def transcribe(
        self, audio_path: Path | str, timestamp_type: ASRTimestampsTypes, timestamps=True, format_output=True
    ):
        """
        Transcribe the audio.

        Args:
            audio_path: Path to audio file.
            timestamp_type: Type of timestamps. Can be ASRTimestampsTypes.FULL_TEXT, ASRTimestampsTypes.SEGMENT, ASRTimestampsTypes.WORD, ASRTimestampsTypes.CHAR.
            timestamps: Specify the need for timestamps. If False, return only text.
            format_output: If False, return a list of timestamps and text fragments. If True, return formatted text with timestamps.
        """
        transcript = self._infer(audio_path, timestamps)
        timestamp_value = timestamp_type.value

        if not timestamps or timestamp_value == "text":
            return transcript.text

        timestamps = transcript.timestamp[timestamp_value]

        if not format_output:
            return timestamps

        output = []
        for stamp in timestamps:
            output.append(f"{stamp['start']:.2f}s - {stamp['end']:.2f}s : {stamp[timestamp_type.value]}")

        return "\n".join(output)
