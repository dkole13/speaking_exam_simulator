"""Generate and validate LLM feedback for submitted answers."""
from typing import Any

from core_utils.constants import REPETITION
from src.asr import count_wer
from src.llm.config import settings
from src.llm.model import get_model
from src.llm.prompts import build_messages
from src.llm.schemas import FeedbackRequest, TaskAnswer


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


def _add_wer_metrics(answers: list[dict[str, TaskAnswer]]) -> list[dict[str, Any]]:
    """
    Calculate WER metrics and add them to repetition answers.

    Args:
        answers: List of answers containing answer_id, db_task, and answer_text.

    Returns:
        A new list of answers filled with WER metrics.
    """
    wer_answers = []

    for answer in answers:
        wer, total_words, ins_rate, del_rate, sub_rate = count_wer(
            hypothesis=answer["answer_text"],
            reference=answer["db_task"],
            format_output=False,
        )

        wer_answer = {
            **answer,
            "wer": {
                "wer": float(wer),
                "total_words": int(total_words),
                "insertion_rate": float(ins_rate),
                "deletion_rate": float(del_rate),
                "substitution_rate": float(sub_rate),
            },
        }

        wer_answers.append(wer_answer)

    return wer_answers


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

    if request.task_type.value == REPETITION:
        messages = build_messages(task_type=task_type, answers=_add_wer_metrics(normalized_answers))
    else:
        messages = build_messages(task_type=task_type, answers=normalized_answers)

    # raw = _call_model(messages)
    # return validate_feedback(
    #     raw_text=raw,
    #     expected_task_type=task_type,
    #     expected_answers=normalized_answers,
    # )
    return _call_model(messages)
