import glob
import sqlite3 as sl

from core_utils.constants import ANSWERS_DIR, DB_PATH
from core_utils.logging_config import setup_logging
from core_utils.timestamps import ASRTimestampsTypes
from src.asr.transcript import ASRModule
from src.db.create_db import create_db
from src.llm.generation import generate_feedback


def select_sample_tasks():
    """Select first task for each task type for demo."""
    conn = sl.connect(DB_PATH)
    transcripts_repetition = conn.execute(
        "SELECT transcription FROM audio_files WHERE (id_task_type=0 AND id_group=1)"
    ).fetchall()
    transcripts_interview = conn.execute(
        "SELECT transcription FROM audio_files WHERE (id_task_type=1 AND id_group=1)"
    ).fetchall()
    conn.close()
    return {"repetition": transcripts_repetition, "interview": transcripts_interview}


if __name__ == "__main__":
    setup_logging()

    if not DB_PATH.exists():
        create_db()

    samples = select_sample_tasks()
    repetition_tasks = samples["repetition"]
    interview_tasks = samples["interview"]

    repetition_audios = glob.glob(str(ANSWERS_DIR / "0.*.wav"))
    interview_audios = glob.glob(str(ANSWERS_DIR / "1.*.wav"))

    asr = ASRModule()  # TODO: disable model's logging
    timestamp_type = ASRTimestampsTypes.SEGMENT

    repetition_transcripts = []
    for audio in repetition_audios:
        repetition_transcripts.append(asr.transcribe(audio_path=audio, timestamp_type=timestamp_type))
    repetition_formatted_tasks = [
        {"db_task": task[0], "answer_id": i + 1, "answer_text": transcript}
        for i, (transcript, task) in enumerate(zip(repetition_transcripts, repetition_tasks, strict=False))
    ]

    interview_transcripts = []
    for audio in interview_audios:
        interview_transcripts.append(asr.transcribe(audio_path=audio, timestamp_type=timestamp_type))
    interview_formatted_tasks = [
        {"db_task": task[0], "answer_id": i + 1, "answer_text": transcript}
        for i, (transcript, task) in enumerate(zip(interview_transcripts, interview_tasks, strict=False))
    ]

    repetition_feedback = generate_feedback("repetition", repetition_formatted_tasks)
    interview_feedback = generate_feedback("interview", interview_formatted_tasks)

    print(repetition_feedback)
    print(interview_feedback)
