from enum import Enum


class ASRTimestampsTypes(Enum):
    """Timestamp types for NVIDIA Parakeet."""

    FULL_TEXT = "full_text"
    SEGMENT = "segment"
    WORD = "word"
    CHAR = "char"

    def __str__(self):
        """Return string representation of timestamp types."""
        return self.value
