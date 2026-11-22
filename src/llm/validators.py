"""Parse model output and validate feedback structure and consistency."""

import json
import re
from typing import Any

from pydantic import ValidationError

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
            raise OutputValidationError("Model output does not contain a JSON object.")
        try:
            return json.loads(cleaned[start : end + 1])
        except json.JSONDecodeError as exc:
            raise OutputValidationError("Model returned invalid JSON.") from exc


def validate_feedback(
    raw_text: str,
    expected_task_type: str,
    expected_answers: list[dict[str, Any]] | None = None,
) -> FeedbackResponse:
    """
    Parse raw text and validate feedback structure and consistency.

    Args:
        raw_text: Raw feedback text returned by the model.
        expected_task_type: Expected value of the feedback task type.
        expected_answers: Optional source answers used for consistency checks.
            Each dictionary is expected to contain "answer_id" and "db_task".
            A missing "answer_text" is treated as an empty string.

    Returns:
        The parsed and validated feedback response.

    Raises:
        OutputValidationError: If JSON extraction or schema validation fails,
        the task type or total score is incorrect, the supplied source
        answers do not contain exactly seven entries, or a compared answer differs from its source.
    """
    data = extract_json(raw_text)
    try:
        result = FeedbackResponse.model_validate(data)
    except ValidationError as exc:
        raise OutputValidationError(f"Feedback schema validation failed: {exc}") from exc

    if result.task_type.value != expected_task_type:
        raise OutputValidationError(f"Wrong task_type: expected {expected_task_type}, got {result.task_type.value}")

    calculated_total = sum(answer.answer_score for answer in result.answers)
    if result.total_score != calculated_total:
        raise OutputValidationError(
            f"Incorrect total_score: model returned {result.total_score}, "
            f"but the sum of answer scores is {calculated_total}."
        )

    if expected_answers is not None:
        if len(expected_answers) != 7:
            raise OutputValidationError(f"Input must contain exactly 7 answers.")
        for generated, source in zip(result.answers, expected_answers):
            source_id = source.get("answer_id")
            source_task = source.get("db_task")
            source_text = source.get("answer_text", "")
            if generated.answer_id != source_id:
                raise OutputValidationError(f"Answer ID mismatch: expected {source_id}, got {generated.answer_id}.")
            if generated.database_task != source_task:
                raise OutputValidationError(f"db_task mismatch for answer {source_id}.")
            if generated.student_answer != source_text:
                raise OutputValidationError(f"student_answer mismatch for answer {source_id}.")
    return result
