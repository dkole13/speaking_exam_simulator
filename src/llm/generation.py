"""Generate and validate LLM feedback for submitted answers."""
from typing import Any

from src.llm.config import settings
from src.llm.model import get_model
from src.llm.prompts import build_messages
from src.llm.schemas import FeedbackRequest
from src.llm.validators import validate_feedback


def _call_model(messages: list[dict[str, str]]) -> str:
    """
    Generate a response using the configured language model.

    Args:
        messages: Chat messages containing roles and content.

    Returns:
        The generated message content with leading and trailing whitespace
        removed.
    """
    response = get_model().create_chat_completion(
        messages=messages,
        temperature=settings.temperature,
        top_k=settings.top_k,
        top_p=settings.top_p,
        max_tokens=settings.max_tokens,
        response_format={"type": "json_object"},
        )
    return response["choices"][0]["message"]["content"].strip()


def generate_feedback(task_type: str, answers: list[dict[str, Any]]):
    """
    Generate and validate feedback for the given task type and answers.

    Args:
        task_type: Type of task for which feedback should be generated.
        answers: Submitted answers, represented as dictionaries.

    Returns:
        The validated feedback returned by validate_feedback.
    """
    request = FeedbackRequest(task_type=task_type, answers=answers)

    normalized_answers = [answer.model_dump() for answer in request.answers]
    messages = build_messages(task_type=task_type, answers=normalized_answers)

    raw = _call_model(messages)
    return validate_feedback(
        raw_text=raw,
        expected_task_type=task_type,
        expected_answers=normalized_answers,
    )
