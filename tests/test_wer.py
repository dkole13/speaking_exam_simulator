import pytest
from src.asr import wer


@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("Hello, WORLD!", "hello world"),
        ("I’m   happy.", "i'm happy"),
        ("  café 123! ", "caf 123"),
    ],
)
def test_normalize(input_text, expected):
    assert wer.normalize(input_text) == expected


@pytest.fixture
def mock_wer(monkeypatch):
    def fake_word_error_rate_detail(hypotheses, references):
        return 0.25, 4, 0.25, 0.0, 0.25

    monkeypatch.setattr(
        wer,
        "word_error_rate_detail",
        fake_word_error_rate_detail,
    )


def test_count_wer_without_formatting(mock_wer):
    result = wer.count_wer(
        "Hello world",
        "Hello the world",
        format_output=False,
    )

    assert result == (0.25, 4, 0.25, 0.0, 0.25)


def test_count_wer_with_formatting(mock_wer):
    output, metrics = wer.count_wer(
        "Hello world",
        "Hello the world",
    )

    assert "WER = 0.25" in output
    assert "total_words = 4" in output
    assert metrics == (4, 0.25, 0.0, 0.25)


def test_count_wer_normalizes_inputs(monkeypatch):
    captured = {}

    def fake_word_error_rate_detail(hypotheses, references):
        captured["hypotheses"] = hypotheses
        captured["references"] = references
        return 0.0, 2, 0.0, 0.0, 0.0

    monkeypatch.setattr(
        wer,
        "word_error_rate_detail",
        fake_word_error_rate_detail,
    )

    wer.count_wer("HELLO!", "Hello", format_output=False)

    assert captured["hypotheses"] == ["hello"]
    assert captured["references"] == ["hello"]
