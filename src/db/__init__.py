"""
Database module for the speaking exam simulator.

Manages SQLite database operations, including schema creation,
clearing the dataset, and inserting audio file metadata with transcriptions.

Public API:
    TaskDatabase: Class for managing database connections and CRUD operations.
    AudioFile: Dataclass representing an audio record and its transcription.
"""

from .audio_db import AudioFile, TaskDatabase


__all__ = ["AudioFile", "TaskDatabase"]
