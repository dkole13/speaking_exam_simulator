import pytest
from unittest.mock import patch

from src.db.create_db import create_db
from core_utils.constants import AUDIO_EXTENSIONS

AUDIO_EXT = next(iter(AUDIO_EXTENSIONS))


@pytest.fixture
def corpus(tmp_path):
    """Provide an empty corpus dir and patch CORPUS_DIR to point at it."""
    root = tmp_path / "corpus"
    root.mkdir()
    with patch("src.db.create_db.CORPUS_DIR", root):
        yield root


@pytest.fixture
def repo():
    """Patch TaskDatabase so no real DB is touched; expose the instance mock."""
    with patch("src.db.create_db.TaskDatabase") as db_cls:
        yield db_cls.return_value


@pytest.fixture
def block(corpus):
    """Factory that creates corpus/<task_type>/<group_id>/ and returns its path."""
    def _make(task_type: str, group_id: str):
        d = corpus / task_type / group_id
        d.mkdir(parents=True, exist_ok=True)
        return d
    return _make


def touch_audio(folder, stem: str, ext: str = AUDIO_EXT):
    """Create an empty audio file. Stem in production is '{type}.{group}.{task}'."""
    (folder / f"{stem}{ext}").write_bytes(b"\x00")


@pytest.mark.parametrize(
    "task_type_dir, task_type_name, id_task_type",
    [("0", "repetition", 0), ("1", "interview", 1)],
)
def test_create_db_parses_audio_file(
    repo, corpus, block, task_type_dir, task_type_name, id_task_type
):
    d = block(task_type_dir, "7")
    touch_audio(d, f'{task_type_dir}.7.3')
    (d / f'{task_type_dir}.7.3.txt').write_text('hi', encoding="utf-8")

    create_db()

    repo.clear_all.assert_called_once()
    repo.add_many.assert_called_once()
    (obj,) = repo.add_many.call_args[0][0]
    assert (obj.task_type, obj.id_task_type) == (task_type_name, id_task_type)
    assert obj.id_group == 7
    assert obj.audio_path == f'{task_type_dir}.7.3'
    assert obj.transcription == "hi"
    assert obj.id_task == 3


@pytest.mark.parametrize(
    "txt_bytes, expected",
    [
        (None, None),
        (b"   \n  ", ""),
        ("hi".encode("cp1251"), "hi"),
    ],
)
def test_create_db_transcription_variants(repo, block, txt_bytes, expected):
    d = block("0", "1")
    touch_audio(d, "0.1.1")
    if txt_bytes is not None:
        (d / "0.1.1.txt").write_bytes(txt_bytes)

    create_db()

    (obj,) = repo.add_many.call_args[0][0]
    assert obj.transcription == expected


def test_create_db_ignores_non_audio_and_garbage(repo, corpus, block):
    (corpus / "readme.txt").write_text("hi")
    d = block("0", "1")
    (d / "readme.md").write_text("hi")
    (d / "notes.txt").write_text("hi")

    create_db()
    repo.add_many.assert_not_called()


def test_create_db_skips_unknown_task_type(repo, block):
    touch_audio(block("2", "1"), "2.1.1")
    create_db()
    repo.add_many.assert_not_called()


@pytest.mark.parametrize(
    "make_tree",
    [
        # non-numeric group directory name
        lambda corpus: (corpus / "0" / "group_a").mkdir(parents=True),
        # non-digit last char in audio file name
        lambda corpus: (
            (corpus / "0" / "1").mkdir(parents=True),
            (corpus / "0" / "1" / f"0.1.x{AUDIO_EXT}").write_bytes(b"\x00"),
        ),
    ],
    ids=["bad_group_name", "bad_file_name"],
)
def test_create_db_invalid_format_raises(repo, corpus, make_tree):
    make_tree(corpus)
    with pytest.raises(ValueError):
        create_db()


@pytest.mark.parametrize(
    "task_type_dir, task_id",
    [
        ("0", 7),   # repetition: tasks 1..7
        ("1", 5),   # interview:  tasks 1..5
    ],
)
def test_create_db_id_task_single_digit(repo, block, task_type_dir, task_id):
    touch_audio(block(task_type_dir, "1"), f"{task_type_dir}.1.{task_id}")
    create_db()

    (obj,) = repo.add_many.call_args[0][0]
    assert obj.id_task == task_id


@pytest.mark.parametrize(
    "task_type_dir, task_id",
    [
        # repetition: tasks 1..7
        ("0", 1), ("0", 2), ("0", 3), ("0", 4), ("0", 5), ("0", 6), ("0", 7),
        # interview: tasks 1..5
        ("1", 1), ("1", 2), ("1", 3), ("1", 4), ("1", 5),
    ],
)
def test_create_db_documents_valid_task_id_range(repo, block, task_type_dir, task_id):
    d = block(task_type_dir, "1")
    touch_audio(d, f"{task_type_dir}.1.{task_id}")
    create_db()
    (obj,) = repo.add_many.call_args[0][0]
    assert obj.id_task == task_id


def test_create_db_accumulates_across_task_types(repo, block):
    touch_audio(block("0", "1"), "0.1.1")
    touch_audio(block("1", "1"), "1.1.1")

    snapshots = []
    repo.add_many.side_effect = lambda items: snapshots.append(
        [a.task_type for a in items]
    )

    create_db()

    assert snapshots[0] == ["repetition"]
    assert sorted(snapshots[1]) == ["interview", "repetition"]
