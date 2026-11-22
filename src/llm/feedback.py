"""Public interface used by the main application."""
from typing import Any

from src.db.audio_db import AudioFile
from src.llm.generation import generate_feedback
from src.llm.schemas import FeedbackResponse


class FeedbackEngine:
    """Provide an interface for generating feedback on submitted answers."""

    def evaluate(self, task: AudioFile, answers: list[dict[str, Any]],) -> FeedbackResponse:
        """
        Evaluate a task and return a feedback response.

        Args:
            task: Audio task containing the task type and transcription.
            answers: Answers to evaluate, represented as dictionaries.

        Returns:
            Structured feedback generated for the given task type and answers.

        Raises:
            ValueError: If the task has no transcription.
        """
        if not task.transcription:
            raise ValueError("The database task has no transcription.")

        return generate_feedback(
            task_type=task.task_type.value,
            answers=answers
        )
