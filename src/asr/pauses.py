from pathlib import Path

import torch
from numpy import mean

from core_utils.constants import VAD_THRESHOLD


def get_pauses(audio_path: Path | str, pause_threshold=VAD_THRESHOLD, format_output=True):
    """
    Get pauses in an audio input.

    Args:
        audio_path (str): Path to audio file.
        pause_threshold (int, optional): Pause threshold. Defaults to VAD_THRESHOLD from core_utils.constants.
        format_output (bool): Specify if the output has to be formatted.
    """
    torch.set_num_threads(1)

    model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad')
    (get_speech_timestamps, _, read_audio, _, _) = utils

    audio = read_audio(str(audio_path))
    speech_timestamps = get_speech_timestamps(audio, model, return_seconds=True)

    end = speech_timestamps[0]['end']
    pauses = []
    for timestamp in speech_timestamps[1:]:
        start = timestamp['start']
        pause = start - end
        end = timestamp['end']
        pauses.append(pause)

    filtered_pauses = [p for p in pauses if p >= pause_threshold]

    if not format_output:
        return {
            'pauses': pauses,
            'filtered_pauses': filtered_pauses,
            'mean_pause_len': mean(pauses),
            'mean_filtered_pause_len': mean(filtered_pauses)
        }

    return \
        f"""Паузы: {filtered_pauses}. Средняя длина пауз больше {pause_threshold}: {mean(filtered_pauses)}."""
