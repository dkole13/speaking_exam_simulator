import logging
from pathlib import Path

from core_utils.constants import AUDIO_EXTENSIONS, CORPUS_DIR, INTERVIEW, REPETITION

from .audio_db import AudioFile, TaskDatabase

logger = logging.getLogger(__name__)


def read_transcription(txt_path: Path) -> str | None:
    """
    Read an audio transcription from file.txt.

    Args:
        txt_path: The path to the txt file with transcription.
    """
    if txt_path.exists():
        try:
            return txt_path.read_text(encoding="utf-8").strip()
        except UnicodeDecodeError:
            return txt_path.read_text(encoding="cp1251").strip()
    logger.info(f'The file {txt_path} does not exist.')
    return None


def create_db():
    """Create database from task corpus."""
    repo = TaskDatabase()
    repo.clear_all()
    logger.info('Database is created!')

    audio_files_to_insert = []

    for task_dir in sorted(CORPUS_DIR.iterdir()):
        if not task_dir.is_dir():
            logger.info(f'The directory {task_dir} does not exist.')
            continue
        if task_dir.name == "0":
            task_type = REPETITION
            id_task_type = 0
        elif task_dir.name == "1":
            task_type = INTERVIEW
            id_task_type = 1
        else:
            logger.info('Undefined directory name.')
            continue

        for group_dir in sorted(task_dir.iterdir()):
            if not group_dir.is_dir():
                logger.info(f'The directory {group_dir} does not exist.')
                continue
            id_group = int(group_dir.name)

            for file_path in sorted(group_dir.iterdir()):
                if file_path.suffix.lower() not in AUDIO_EXTENSIONS:
                    logger.info(f'The extension of {file_path} is not supported. ')
                    continue
                txt_path = file_path.with_suffix(".txt")

                transcription = read_transcription(txt_path)

                file_name = str(file_path.stem)
                audio_obj = AudioFile(
                    task_type=task_type,
                    audio_path=file_name,
                    id_group=id_group,
                    transcription=transcription,
                    id_task_type=id_task_type,
                    id_task=int(file_name[-1:]),
                )

                audio_files_to_insert.append(audio_obj)

        if audio_files_to_insert:
            repo.add_many(audio_files_to_insert)
            logger.info('Database is filled!')


if __name__ == "__main__":
    create_db()
