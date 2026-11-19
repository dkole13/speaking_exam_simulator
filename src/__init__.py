"""Speaking trainer: practice for the speaking section of language exams.

The user gets a task (currently TOEFL iBT: Listen and Repeat, Take an
Interview), records an answer, and receives feedback based on the
recognized speech.

Subpackages:
    db: models and repositories.
    asr: speech recognition behind a common interface.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("speaking-trainer")
except PackageNotFoundError:
    __version__ = "0.0.0"
