"""Build task-specific chat messages."""

import json
from typing import Any

from core_utils.constants import INTERVIEW, REPETITION
from src.llm.prompt_templates import (
    LISTEN_AND_REPEAT_PROMPT,
    TAKE_AN_INTERVIEW_PROMPT,
)

PROMPTS = {
    REPETITION: LISTEN_AND_REPEAT_PROMPT,
    INTERVIEW: TAKE_AN_INTERVIEW_PROMPT,
}


def build_messages(task_type: str, answers: list[dict[str, Any]]) -> list[dict[str, str]]:
    """
    Build system and user messages for the specified speaking task.

    Args:
        task_type: Task type identifying the prompt template. Supported values are "repetition" and "interview".
        answers: Answer dictionaries to serialize and include in the prompt.

    Returns:
        Two chat messages in order: the system instructions and the user
        prompt containing the serialized answers.

    Raises:
        ValueError: If the task type is not supported.
    """
    if task_type not in PROMPTS:
        raise ValueError(f"Unsupported task type: {task_type}")

    answers_json = json.dumps(answers, ensure_ascii=False, indent=2)
    prompt = PROMPTS[task_type]
    user_prompt = prompt["USER_PROMPT"].format(answers=answers_json)
    return [
        {"role": "system", "content": prompt["SYSTEM_PROMPT"]},
        {"role": "user", "content": user_prompt},
    ]
