from typing import cast
from unittest.mock import MagicMock, patch

import pytest

from core_utils.constants import INTERVIEW, REPETITION
from src.llm.generation import _add_wer_metrics, _call_model, generate_feedback
from src.llm.schemas import TaskAnswer


@pytest.fixture
def mock_model():
    """Patch get_model() with mock."""
    with patch("src.llm.generation.get_model") as mock_get:
        model = MagicMock()
        model.create_chat_completion.return_value = {
            "choices": [{"message": {"content": "feedback content"}}]
        }
        mock_get.return_value = model
        yield model


@pytest.fixture
def mock_settings():
    with patch("src.llm.config.Settings") as s:
        s.temperature = 0.2
        s.top_k = 50
        s.top_p = 0.9
        s.max_tokens = 2048
        yield s


@pytest.fixture
def sample_answers() -> list[dict[str, TaskAnswer]]:
    return cast(
        list[dict[str, TaskAnswer]],
        [
            {"answer_id": 1, "db_task": "hello world", "answer_text": "hello word"},
            {"answer_id": 2, "db_task": "foo bar", "answer_text": "foo bar"},
        ],
    )


def test_returns_stripped_content(mock_model, mock_settings):
    result = _call_model([{"role": "user", "content": "hi"}])
    assert result == "feedback content"


def test_adds_wer_dict(sample_answers):
    with patch("src.asr.count_wer") as mock_wer:
        mock_wer.return_value = (0.5, 2, 0.0, 0.0, 0.5)
        result = _add_wer_metrics(sample_answers)

    assert len(result) == 2
    assert result[0]["wer"] == {
        "wer": 0.5,
        "total_words": 2,
        "insertion_rate": 0.0,
        "deletion_rate": 0.0,
        "substitution_rate": 0.5,
    }
    assert result[0]["answer_id"] == 1
    assert result[0]["answer_text"] == "hello word"


def test_empty_input():
    assert _add_wer_metrics([]) == []


def test_repetition_uses_wer_metrics(mock_model, mock_settings, sample_answers):
    request_mock = MagicMock()
    request_mock.task_type.value = REPETITION
    request_mock.answers = [
        MagicMock(model_dump=MagicMock(return_value=ans)) for ans in sample_answers
    ]

    with patch("src.llm.generation.FeedbackRequest", return_value=request_mock), \
         patch("src.llm.generation._add_wer_metrics") as mock_add_wer, \
         patch("src.llm.generation.build_messages") as mock_build:

        mock_build.return_value = [{"role": "user", "content": "p"}]
        generate_feedback(REPETITION, sample_answers)

    mock_add_wer.assert_called_once_with(sample_answers)


# def test_should_validate_model_output(mock_model, mock_settings, sample_answers):
#     task_type = INTERVIEW
#     request_mock = MagicMock()
#     request_mock.task_type.value = task_type
#     request_mock.answers = [
#         MagicMock(model_dump=MagicMock(return_value=ans)) for ans in sample_answers
#     ]
#
#     with patch("src.llm.schemas.FeedbackRequest", return_value=request_mock), \
#             patch("src.llm.prompts.build_messages",
#                   return_value=[{"role": "user", "content": "p"}]), \
#             patch("src.llm.validators.validate_feedback",
#                   return_value={"ok": True}) as mock_validate:
#         generate_feedback(task_type, sample_answers)
#
#     mock_validate.assert_called_once_with(
#         raw_text="feedback content",
#         expected_task_type=task_type,
#         expected_answers=sample_answers,
#     )
