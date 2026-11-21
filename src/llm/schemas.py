"""Pydantic schemas for task input and generated speaking feedback."""

from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


class TaskType(str, Enum):
    REPETITION = "repetition"
    INTERVIEW = "interview"


class TaskAnswer(BaseModel):
    """One response and its matching source item from the database.

    For repetition, database_task is the reference sentence.
    For interview, database_task is the interview question.
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    answer_id: int = Field(ge=1)
    db_task: str = Field(min_length=1)
    answer_text: str = Field(description="ASR transcript for this answer; may be empty if no speech was recognized.")


class FeedbackRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    task_type: TaskType
    answers: list[TaskAnswer]


class Criterion(BaseModel):
    comment: str
    evidence: list[str] = Field(default_factory=list)


class AnswerFeedback(BaseModel):
    """Feedback for one answer within a task."""

    answer_id: int = Field(ge=1)
    db_task: str
    student_answer: str
    answer_score: int = Field(ge=0, le=5)
    criteria: dict[str, Criterion]
    # strengths: list[str] = Field(default_factory=list)
    # improvements: list[str] = Field(default_factory=list)
    # corrected_or_suggested_answer: str


class FeedbackResponse(BaseModel):
    """Complete feedback returned from one model call for one task."""

    model_config = ConfigDict(str_strip_whitespace=True)

    task_type: TaskType
    answers: list[AnswerFeedback]
    total_score: int = Field(ge=0)
    max_score: int = Field(gt=0)
    # overall_comment: str
    # disclaimer: str = "Ответ сгенерирован ИИ. Не является официальной оценкой TOEFL."
