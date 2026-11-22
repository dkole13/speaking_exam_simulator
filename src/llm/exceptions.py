class FeedbackError(Exception):
    """Base exception for the feedback package."""


class GenerationError(FeedbackError):
    """Raised when the model cannot produce a usable response."""


class OutputValidationError(FeedbackError):
    """Raised when generated feedback does not match the expected schema."""
