# Speaking Exam Simulator

The project is aimed at helping the user prepare for the speaking section of international 
language exams (specifically TOEFL iBT as of 2026). It includes a database of tasks of all types
(Listen and Repeat, Take an Interview), does ASR and then provides LLM-based feedback. This project doesn't require GPU.

## Tech Stack

- **Runtime**: Python 3.13.
- **Package Manager**: uv.
- **ASR**: NVIDIA NeMo + Parakeet TDT 0.6B (Automatic Speech Recognition).
- **LLM**: llama-cpp-python + LiquidAI LFM2.5-1.2B-Instruct (Local LLM Inference, available for CPU).
- **Data Validation**: Pydantic.
- **Database**: SQLite.

## Quick Start

### Prerequisites

- **Python**: 3.13 or later.
- **uv**: Python package and project dependency manager.
- **Git**: For cloning the repository.
- **CMake**: Optional; Required if llama-cpp-python needs to be built from source.
- **C++ Compiler**: Optional; Required for building llama-cpp-python from source.
- **Internet Connection**: Required for downloading pretrained models from Hugging Face.
- **GPU**: Optional; the project supports CPU-only inference.

### 1. Installation

1. Clone the repository:
```bash
git clone https://github.com/dkole13/speaking_exam_simulator
```

2. Install uv (only required if uv is not installed globally):
```bash
pip install uv
```

3. Environment setup:
```bash
uv init venv
```

4. Install dependencies via uv:
```bash
uv sync
```

### 2. Configure models

The project uses the following models:

- **ASR:** `nvidia/parakeet-tdt-0.6b-v2`
- **LLM:** `LiquidAI/LFM2.5-1.2B-Instruct-GGUF`

#### ASR model

You can download the [ASR model](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v2) manually and place it in the `models/` directory using the following filename:

```text
models/
└── parakeet-tdt-0.6b-v2.nemo
```

Alternatively, the model will be downloaded automatically on the first run if it is not found in the directory.

#### LLM model

[The GGUF language model](https://huggingface.co/LiquidAI/LFM2.5-1.2B-Instruct-GGUF) is loaded from Hugging Face using `Llama.from_pretrained()` from the `llama-cpp-python` library.

The model is downloaded automatically on the first run if it is not already available in the local Hugging Face cache. Subsequent runs reuse the cached model, so it does not need to be downloaded again.

The default model configuration is:

- **Repository:** `LiquidAI/LFM2.5-1.2B-Instruct-GGUF`
- **Filename:** `LFM2.5-1.2B-Instruct-Q4_K_M.gguf`
- **Context size:** `4096` tokens

You can customize the repository ID and model filename using the `MODEL_REPO_ID` and `MODEL_FILENAME` environment variables.

### 3. Run the application

On Unix-like systems (Linux and macOS), you can use the commands provided in the `Makefile`.

To start the application, run the corresponding command from the `Makefile`.

Alternatively, you can launch it directly:

```bash
uv run python start.py
```

The code should return an answer in JSON-format. For example:

#### Input

```bash
"answers": [
    {
      "answer_id": 1,
      "db_task": 'Thank you for speaking with me today. Now, think back to the most recent celebration you took part 
      in—this could be a holiday, birthday, festival, or any special gathering. What was the reason for the celebration? 
      What moments or details made it enjoyable for you?',
      "answer_text": 'The last big event I attended was my cousin’s wedding about six months ago. He married his fiance, 
      and it was a really wonderful, just beautiful, experience. Family members came from all over the world to attend. 
      Some of them actually came from other continents and I hadn’t seen them for an extremely long time. Accordingly, 
      while the main purpose of the wedding was to celebrate their marriage, what I liked the most, actually, was the 
      opportunity to reconnect with my relatives and loved ones to share stories about my life and their lives. In that 
      way I realized that, you know, I have a lot of relatives who I can depend on. I think even my cousin and his 
      fiance appreciated that realization as well, even though, like, the whole point of the event was to celebrate 
      their love and commitment to one another.'
    },
    {
      "answer_id": 2,
      "db_task": ...,
      "answer_text": ...
     }
]
```

#### Output

```bash
{
  "task_type": "interview",
  "answers": [
    {
      "answer_id": 1,
      "db_task": 'Thank you for speaking with me today. Now, think back to the most recent celebration you took part 
      in—this could be a holiday, birthday, festival, or any special gathering. What was the reason for the celebration? 
      What moments or details made it enjoyable for you?',
      "student_answer": 'The last big event I attended was my cousin’s wedding about six months ago. He married his fiance, 
      and it was a really wonderful, just beautiful, experience. Family members came from all over the world to attend. 
      Some of them actually came from other continents and I hadn’t seen them for an extremely long time. Accordingly, 
      while the main purpose of the wedding was to celebrate their marriage, what I liked the most, actually, was the 
      opportunity to reconnect with my relatives and loved ones to share stories about my life and their lives. In that 
      way I realized that, you know, I have a lot of relatives who I can depend on. I think even my cousin and his 
      fiance appreciated that realization as well, even though, like, the whole point of the event was to celebrate 
      their love and commitment to one another.'
      "answer_score": 4,
      "criteria": {
        "fluency": "Краткое поведение, хороший темп с паузами, достаточно сложный слова и конструкций.",
        "vocabulary and grammar": "Хорошая проработка слова и грамматики, но могут быть некоторые ошибки в формизации.",
        "organization": "Вывод очень понятен, структура ответ проряется, но быстрее бывает короче."
      }
    },
    {
      "answer_id": 2,
      "db_task": ...
      "student_answer": ...
      "answer_score": int,
      "criteria": {
        "fluency": ...
        "vocabulary and grammar": ...
        "organization": ...
        }
    }
    ...
    ],
  "total_score": int,
  "max_score": 20
}
```

### 4. Environment variables

You can customize model settings by creating a `.env` file in the project root.

If no `.env` file is provided, the default configuration values are used.

Settings available in `constants.py` include:

- `MODEL_REPO_ID` — Hugging Face repository ID of the LLM.
- `MODEL_FILENAME` — GGUF model filename.
- `MODEL_N_CTX` — LLM context size.
- `MODEL_N_THREADS` — number of CPU threads.
- `MODEL_VERBOSE` — enable or disable verbose model output.
- `LLM_TEMPERATURE` — generation temperature.
- `LLM_TOP_K` — top-k sampling parameter.
- `LLM_TOP_P` — top-p sampling parameter.
- `LLM_MAX_TOKENS` — maximum number of generated tokens.


## Data

The project uses publicly available TOEFL Speaking practice materials and scoring guidelines from the following sources:

- **Practice Questions and Answers:** [TOEFL® Speaking Practice Questions and Answers (2026)](https://www.toeflresources.com/speaking-section/toefl-speaking-samples/)
by Michael Goodine. The dataset includes audio recordings, transcripts, and sample questions for both
*Listen and Repeat* and *Take an Interview* tasks.

- **Scoring Criteria:** [How Is TOEFL Speaking Scored in 2026? The Rubric, Decoded](https://www.myspeakingscore.com/blog/how-toefl-speaking-is-scored)
by My Speaking Score. This resource was used as a reference for defining the evaluation criteria and scoring approach
for both speaking task types.

The original materials were adapted and organized into a local dataset for the project. The evaluation criteria were also adapted to support automated feedback generation using a local language model. The resulting scoring system is intended for practice and educational purposes and does not represent an official TOEFL or ETS scoring system.

## Contributing

We welcome contributions from developers who want to improve Speaking Exam Simulator!
Follow these steps to contribute effectively:

1. Fork the repository

- Click the `Fork` button on GitHub to create your own copy of the project.

2. Clone your fork:

```bash
git clone https://github.com/yourusername/speaking_exam_simulator
```

3. Create a feature branch:

```bash
git checkout -b 'your-feature-name'
```

4. Set up the environment:

- Follow the setup instructions in the `README` to install dependencies and configure your `.env` files.
5. Follow code style and formatting files. Ensure consistent formatting before committing:

```bash
uv run ruff check
```

Alternatively, it is ensured automatically by pre-commit.

6. Use clear commit messages.


7. Write or update tests.


8. Document your changes:

- Update or add `README.md`, `CHANGELOG.md`, or `CONTRIBUTING.md` if needed.
Submit a `Pull Request (PR)`

9. Push your branch and open a PR with:
- A short, clear description of your changes.
- Any related issue numbers (for example, “Closes #12”).
- Screenshots or example outputs (if applicable).
- Participate in Code Review

Respond to feedback, make improvements, and help maintain project quality.



## License

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**. You can find the full license text in 
the [LICENSE](https://github.com/dkole13/speaking_exam_simulator/blob/main/LICENSE.txt) file.

You are free to use, study, modify, and redistribute this software under the terms of the GNU GPL v3.0.

The license applies only to the original source code developed for this project. Third-party datasets, audio recordings, 
transcripts, pretrained models, and dependencies are subject to their respective licenses and terms of use.
