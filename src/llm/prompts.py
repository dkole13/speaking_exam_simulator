"""Build task-specific chat messages."""

import json
from typing import Any

from src.llm.prompt_templates import (
    LISTEN_AND_REPEAT_PROMPT,
    TAKE_AN_INTERVIEW_PROMPT,
)


PROMPTS = {
    "repetition": LISTEN_AND_REPEAT_PROMPT,
    "interview": TAKE_AN_INTERVIEW_PROMPT,
}


def build_messages(
    task_type: str,
    answers: list[dict[str, Any]]
) -> list[dict[str, str]]:

    if hasattr(task_type, "value"):
        task_type = task_type.value

    if task_type not in PROMPTS:
        raise ValueError(f"Unsupported task type: {task_type}")

    answers_json = json.dumps(answers, ensure_ascii=False, indent=2)
    prompt = PROMPTS[task_type]
    user_prompt = prompt["USER_PROMPT"].format(answers=answers_json)
    return [
        {"role": "system", "content": prompt["SYSTEM_PROMPT"]},
        {"role": "user", "content": user_prompt},
    ]
