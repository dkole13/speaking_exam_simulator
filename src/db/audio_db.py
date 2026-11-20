import sqlite3 as sl
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

DB_PATH = Path(__file__).parent.parent.parent / "task_corpus" / "audio_files.db"


@dataclass
class AudioFile:
    """
    Represents an audio file and its associated data in the dataset.

    Attributes:
        task_type: The type of the task.
        audio_path: The path to the audio file.
        id_task_type: The task type ID.
        id_group: The group ID.
        id_task: The task ID.
        transcription: The text transcription.
        id: The unique database ID.
    """

    task_type: Optional[str] = None
    audio_path: Optional[str] = None
    id_task_type: Optional[int] = None
    id_group: Optional[int] = None
    id_task: Optional[int] = None
    transcription: Optional[str] = None
    id: Optional[int] = None


class TaskDatabase:
    """A class that creates the database with tasks."""

    def __init__(self, db_path: Path = DB_PATH):
        """
        Initialize an instance of TaskDatabase.

        Args:
            db_path (Path): Path to the database with tasks
        """
        self.db_path = db_path
        self._init_schema()

    @contextmanager
    def _conn(self):
        """
        Open a database connection for a 'with' block.

        Yields:
            sqlite3.Connection: The database connection.
        """
        conn = sl.connect(self.db_path)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init_schema(self) -> None:
        """Create the 'audio_files' table if it does not exist."""
        with self._conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS audio_files (
                    id INTEGER PRIMARY KEY CHECK (id > 0),
                    task_type TEXT NOT NULL,
                    id_task_type INTEGER,
                    id_group INTEGER,
                    id_task INTEGER,
                    audio_path TEXT NOT NULL,
                    transcription TEXT
                    )
                """)

    def add(self, audio_file: AudioFile) -> None:
        """Add a single audio file record to the dataset."""
        with self._conn() as conn:
            conn.execute("""
                INSERT INTO audio_files
                (task_type, id_task_type, id_group, id_task, audio_path, transcription)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                audio_file.task_type,
                audio_file.id_task_type,
                audio_file.id_group,
                audio_file.id_task,
                audio_file.audio_path,
                audio_file.transcription
            ))

    def add_many(self, audio_files: list[AudioFile]) -> None:
        """Add multiple audio file records to the dataset in a single transaction."""
        with self._conn() as conn:
            conn.executemany("""
                INSERT INTO audio_files
                (task_type, id_task_type, id_group, id_task, audio_path, transcription)
                VALUES (?, ?, ?, ?, ?, ?)
            """, [
                (
                    f.task_type,
                    f.id_task_type,
                    f.id_group,
                    f.id_task,
                    f.audio_path,
                    f.transcription
                ) for f in audio_files
            ])

    def clear_all(self) -> None:
        """Delete all records from the 'audio_files' table."""
        with self._conn() as conn:
            conn.execute("DELETE FROM audio_files")
