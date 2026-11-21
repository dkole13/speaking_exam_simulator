"""Public interface used by the main application."""
from typing import Any

from src.db.audio_db import AudioFile

from src.llm.generation import generate_feedback
from src.llm.schemas import FeedbackResponse


class FeedbackEngine:

    def evaluate(self, task: AudioFile, answers: list[dict[str, Any]],) -> FeedbackResponse:

        if not task.transcription:
            raise ValueError("The database task has no transcription.")

        return generate_feedback(
            task_type=task.task_type.value,
            answers=answers
        )
