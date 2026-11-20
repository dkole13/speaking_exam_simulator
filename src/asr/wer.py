import re

from nemo.collections.asr.metrics.wer import word_error_rate_detail


def normalize(text: str) -> str:
    """
    Normalize text: remove punctuation, cast to lowercase.

    Args:
        text: text to normalize
    """
    text = text.lower().replace("’", "'")
    text = re.sub(r"[^a-z0-9' ]+", " ", text)
    return " ".join(text.split())


def count_wer(hypothesis, reference, format_output=True):
    """
    Count WER with feedback: total words, insertion rate, deletion rate, subtraction rate.

    Args:
        hypothesis: hypothesis text
        reference: reference text
        format_output: If False, returns metrics only. If True, returns metrics along with a formatted report.
    """
    wer, n_words, ins_rate, del_rate, sub_rate = word_error_rate_detail(
        hypotheses=[normalize(hypothesis)], references=[normalize(reference)]
    )

    if not format_output:
        return wer, n_words, ins_rate, del_rate, sub_rate

    output = f"""WER = {wer}
    total_words = {n_words}
    insertion_rate = {ins_rate}
    deletion_rate = {del_rate}
    subtraction_rate = {sub_rate}"""

    return output, (n_words, ins_rate, del_rate, sub_rate)
