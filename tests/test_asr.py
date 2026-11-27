from pathlib import Path
from unittest.mock import MagicMock

import pytest

from src.asr import transcript
from core_utils.timestamps import ASRTimestampsTypes


@pytest.fixture
def asr():
    """Create ASRModule without loading a real model."""
    instance = transcript.ASRModule.__new__(transcript.ASRModule)
    instance._model_name = "test-model"
    instance._model_path = Path("test-model.nemo")
    instance._model = MagicMock()
    return instance


def test_init_model_restores_local_model(asr, monkeypatch):
    asr._model_path = MagicMock()
    asr._model_path.exists.return_value = True

    restore_mock = MagicMock(return_value="restored-model")

    monkeypatch.setattr(
        transcript.nemo_asr.models.ASRModel,
        "restore_from",
        restore_mock,
    )

    result = asr._init_model()

    assert result == "restored-model"
    restore_mock.assert_called_once_with(
        restore_path=asr._model_path
    )


def test_init_model_downloads_pretrained_model(asr, monkeypatch):
    asr._model_path = MagicMock()
    asr._model_path.exists.return_value = False

    pretrained_mock = MagicMock(return_value="pretrained-model")

    monkeypatch.setattr(
        transcript.nemo_asr.models.ASRModel,
        "from_pretrained",
        pretrained_mock,
    )

    result = asr._init_model()

    assert result == "pretrained-model"
    pretrained_mock.assert_called_once_with(
        model_name=asr._model_name
    )


def test_transcribe_without_timestamps(asr):
    transcript = MagicMock()
    transcript.text = "hello world"
    asr._infer = MagicMock(return_value=transcript)

    result = asr.transcribe(
        "audio.wav",
        ASRTimestampsTypes.WORD,
        timestamps=False,
    )

    assert result == "hello world"
    asr._infer.assert_called_once_with("audio.wav", False)


def test_transcribe_returns_raw_timestamps(asr):
    timestamps = [
        {"start": 0.1, "end": 0.5, "word": "hello"},
        {"start": 0.6, "end": 1.0, "word": "world"},
    ]

    transcript = MagicMock()
    transcript.timestamp = {"word": timestamps}
    asr._infer = MagicMock(return_value=transcript)

    result = asr.transcribe(
        "audio.wav",
        ASRTimestampsTypes.WORD,
        format_output=False,
    )

    assert result == timestamps


def test_transcribe_formats_timestamps(asr):
    timestamps = [
        {"start": 0.1, "end": 0.5, "word": "hello"},
        {"start": 0.6, "end": 1.0, "word": "world"},
    ]

    transcript = MagicMock()
    transcript.timestamp = {"word": timestamps}
    asr._infer = MagicMock(return_value=transcript)

    result = asr.transcribe(
        "audio.wav",
        ASRTimestampsTypes.WORD,
        format_output=True,
    )

    assert result == (
        "0.10s - 0.50s : hello\n"
        "0.60s - 1.00s : world"
    )
