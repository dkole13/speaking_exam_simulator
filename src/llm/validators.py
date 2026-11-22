
"""Parse model output and validate feedback structure and consistency."""

import json
import re
from typing import Any

from pydantic import ValidationError

from core_utils.constants import (
    ANSWERS_PER_TASK,
    MAX_TASK_SCORE,
    SUPPORTED_TASK_TYPES,
)

from src.llm.schemas import FeedbackResponse
from src.llm.exceptions import OutputValidationError


def extract_json(text: str) -> dict:
    """
    Parse raw JSON, tolerating accidental Markdown fences or surrounding text.

    Args:
        text: Raw text returned by the model.

    Returns:
        The parsed JSON value, expected to be a dictionary.

    Raises:
        OutputValidationError: If initial parsing fails and no brace-delimited
        JSON object can be found, or if the extracted substring is invalid JSON.
    """
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start < 0 or end <= start:
            raise OutputValidationError("Model output does not contain a JSON object.") from None


def _normalize_task_type(task_type: str) -> str:
    """
    Normalize and validate the task type.

    Args:
        task_type: Task type as a string or Enum value.

    Returns:
        Normalized task type string.

    Raises:
        OutputValidationError: If the task type is unsupported.
    """
    if hasattr(task_type, "value"):
        task_type = task_type.value
    if task_type not in SUPPORTED_TASK_TYPES:
        raise OutputValidationError(f"Unsupported task type: {task_type}.")
    return task_type


def _parse_feedback(data: dict) -> FeedbackResponse:
    """
    Validate the structure of the generated feedback.

    Args:
        data: Parsed JSON object returned by the model.

    Returns:
        Validated FeedbackResponse instance.

    Raises:
        OutputValidationError: If the data does not match the schema.
    """
    try:
        return FeedbackResponse.model_validate(data)
    except ValidationError as exc:
        raise OutputValidationError(f"Feedback schema validation failed: {exc}") from exc


def _validate_task_type(result: FeedbackResponse, expected_task_type: str) -> None:
    """
    Check whether the generated feedback has the expected task type.

    Args:
        result: Validated feedback response.
        expected_task_type: Expected task type.

    Raises:
        OutputValidationError: If the task types do not match.
    """
    actual_task_type = result.task_type.value

    if actual_task_type != expected_task_type:
        raise OutputValidationError(f"Wrong task_type: expected {expected_task_type}, got {actual_task_type}.")


def _validate_answer_count(result: FeedbackResponse, expected_task_type: str) -> None:
    """
    Check the number of answers in the generated feedback.

    Args:
        result: Validated feedback response.
        expected_task_type: Task type determining the required count.

    Raises:
        OutputValidationError: If the number of answers is incorrect.
    """
    expected_count = ANSWERS_PER_TASK[expected_task_type]
    actual_count = len(result.answers)
    if actual_count != expected_count:
        raise OutputValidationError(f"Incorrect number of answers: expected {expected_count}, got {actual_count}.")


def _validate_scores(result: FeedbackResponse, expected_task_type: str) -> None:
    """
    Validate the maximum and total task scores.

    Args:
        result: Validated feedback response.
        expected_task_type: Task type determining the maximum score.

    Raises:
        OutputValidationError: If max_score or total_score is incorrect.
    """
    expected_max_score = MAX_TASK_SCORE[expected_task_type]
    if result.max_score != expected_max_score:
        raise OutputValidationError(f"Incorrect max_score: expected {expected_max_score}, got {result.max_score}.")

    calculated_total = sum(answer.answer_score for answer in result.answers)
    if result.total_score != calculated_total:
        raise OutputValidationError(f"Incorrect total_score: model returned {result.total_score}, "
                                    f"but the sum of answer scores is {calculated_total}.")


def _validate_source_answers(
    result: FeedbackResponse,
    expected_answers: list[dict[str, Any]],
    expected_task_type: str,
) -> None:
    """
    Compare generated feedback with the original input answers.

    Checks the number of answers, their identifiers, source tasks,
    and ASR transcriptions. The original order must be preserved.

    Args:
        result: Validated feedback response.
        expected_answers: Original answers supplied to the model.
        expected_task_type: Task type determining the required count.

    Raises:
        OutputValidationError: If the input count or any answer data
            differs from the generated feedback.
    """
    expected_count = ANSWERS_PER_TASK[expected_task_type]
    if len(expected_answers) != expected_count:
        raise OutputValidationError(f"Input must contain exactly {expected_count} "
                                    f"answers for task '{expected_task_type}'.")

    for generated, source in zip(result.answers, expected_answers, strict=True):
        _validate_single_answer(generated, source)


def _validate_single_answer(generated: Any,source: dict[str, Any]) -> None:
    """
    Compare one generated answer with its original input.

    Args:
        generated: Generated AnswerFeedback instance.
        source: Original answer dictionary.

    Raises:
        OutputValidationError: If the answer ID, db_task,
            or student transcription does not match.
    """
    source_id = source.get("answer_id")
    source_task = source.get("db_task")
    source_text = source.get("answer_text", "")

    if generated.answer_id != source_id:
        raise OutputValidationError(f"Answer ID mismatch: expected {source_id}, got {generated.answer_id}.")

    if generated.db_task != source_task:
        raise OutputValidationError(f"db_task mismatch for answer {source_id}.")

    if generated.student_answer != source_text:
        raise OutputValidationError(f"student_answer mismatch for answer {source_id}.")


def validate_feedback(
    raw_text: str,
    expected_task_type: str,
    expected_answers: list[dict[str, Any]] | None = None,
) -> FeedbackResponse:
    """
    Parse and validate the complete feedback returned by the model.

    Args:
        raw_text: Raw feedback text returned by the model.
        expected_task_type: Expected task type.
        expected_answers: Optional original answers used for consistency
            checks. Each dictionary contains answer_id, db_task,
            and answer_text.

    Returns:
        Parsed and validated FeedbackResponse instance.

    Raises:
        OutputValidationError: If JSON parsing, schema validation,
            task type, answer count, scoring, or source consistency
            checks fail.
    """
    task_type = _normalize_task_type(expected_task_type)
    data = extract_json(raw_text)
    result = _parse_feedback(data)

    _validate_task_type(result, task_type)
    _validate_answer_count(result, task_type)
    _validate_scores(result, task_type)

    if expected_answers is not None:
        _validate_source_answers(result, expected_answers, task_type)

    return result
