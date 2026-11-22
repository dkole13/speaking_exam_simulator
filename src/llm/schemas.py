"""Pydantic schemas for task input and generated speaking feedback."""

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from core_utils.constants import (
    MAX_ANSWER_SCORE,
    MIN_ANSWER_SCORE,
)


class TaskType(str, Enum):
    """
    Supported speaking task types.

    Attributes:
        REPETITION: A task in which the student repeats a reference sentence.
        INTERVIEW: A task in which the student answers an interview question.
    """

    REPETITION = "repetition"
    INTERVIEW = "interview"


class TaskAnswer(BaseModel):
    """
    One response and its matching source item from the database.

    Attributes:
        answer_id: Answer identifier, which must be at least 1.
        db_task: Non-empty reference sentence for a repetition task or interview question for an interview task.
        answer_text: ASR transcript of the student's answer. May be empty if no speech was recognized.
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    answer_id: int = Field(ge=1)
    db_task: str = Field(min_length=1)
    answer_text: str = Field(description="ASR transcript for this answer; may be empty if no speech was recognized.")


class FeedbackRequest(BaseModel):
    """
    Input data for generating feedback on a speaking task.

    Attributes:
        task_type: Type of speaking task to evaluate.
        answers: Student answers paired with their source database items.
    """

    task_type: TaskType
    answers: list[TaskAnswer]


class Criterion(BaseModel):
    """
    Evaluation of a single criterion.

    Attributes:
        comment: Feedback explaining the evaluation.
        evidence: Supporting text excerpts or observations. Defaults to an empty list.
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    comment: str
    evidence: list[str] = Field(default_factory=list)


class AnswerFeedback(BaseModel):
    """
    Generated feedback for one answer within a speaking task.

    Attributes:
        answer_id: Identifier of the evaluated answer, which must be at least 1.
        db_task: Source reference sentence or interview question.
        student_answer: Transcript of the student's answer.
        answer_score: Score assigned to the answer, from 0 to 5 inclusive.
        criteria: Evaluations indexed by criterion name.
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    answer_id: int = Field(ge=1)
    db_task: str
    student_answer: str
    answer_score: int = Field(ge=MIN_ANSWER_SCORE, le=MAX_ANSWER_SCORE)
    criteria: dict[str, Criterion]


class FeedbackResponse(BaseModel):
    """
    Complete feedback generated for one speaking task.

    Attributes:
        task_type: Type of speaking task evaluated.
        answers: Individual feedback entries for the student's answers.
        total_score: Non-negative total score reported for the task.
        max_score: Positive maximum possible score for the task.
    """

    task_type: TaskType
    answers: list[AnswerFeedback]
    total_score: int = Field(ge=0)
    max_score: int = Field(gt=0)
