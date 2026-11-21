"""LLM generation."""
from typing import Any

from src.llm.schemas import FeedbackRequest
from src.llm.config import settings
from src.llm.model import get_model
from src.llm.prompts import build_messages
from src.llm.validators import validate_feedback


def _call_model(messages: list[dict[str, str]]) -> str:
    response = get_model().create_chat_completion(
        messages=messages,
        temperature=settings.temperature,
        top_p=settings.top_p,
        max_tokens=settings.max_tokens,
        response_format={"type": "json_object"},
        )
    return response["choices"][0]["message"]["content"].strip()


def generate_feedback(
    task_type: str,
    answers: list[dict[str, Any]]
):
    request = FeedbackRequest(
        task_type=task_type,
        answers=answers,
    )

    normalized_answers = [answer.model_dump() for answer in request.answers]
    messages = build_messages(
        task_type=task_type,
        answers=normalized_answers,
    )
    raw = _call_model(messages)
    return validate_feedback(
        raw_text=raw,
        expected_task_type=task_type,
        expected_answers=normalized_answers,
    )
