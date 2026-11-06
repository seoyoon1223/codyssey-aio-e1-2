# Python and Computer Fundamentals Quiz Game

A small console quiz game for revisiting Python and basic computer science concepts. The initial questions cover Python syntax, built-in types, operators, and common functions. These topics were chosen because short recall questions make it easy to review foundational concepts and add new questions without changing the program.

## Environment

| Item | Version or value |
| --- | --- |
| Operating system | Windows 11 |
| Shell | PowerShell |
| Python | 3.12.14 |
| Git | 2.56.0.windows.4 |
| uv | 0.13.7 |
| Runtime dependencies | Python standard library only |

The project uses PEP 621 metadata in `pyproject.toml`. The `src/quiz_game` package follows the `src` layout. `uv.lock` records the environment; no third-party runtime package is needed.

## Run

```powershell
uv sync --no-install-project
uv run --no-sync python main.py
```

The menu provides five actions:

1. Play every registered quiz.
2. Add a quiz with four choices and a numbered answer.
3. List registered quiz questions.
4. Show the best score.
5. Save and exit.

Blank text, nonnumeric values, and numbers outside the allowed range are rejected with a retry prompt. EOF and Ctrl+C stop safely and save the current state.

## Implementation

`Quiz` validates each question, four nonempty choices, and an answer from 1 through 4. `QuizGame` owns the menu, quiz flow, score, and user interaction. `storage.py` loads and saves state as UTF-8 JSON. Saving uses a temporary file followed by an atomic replace so an interrupted write does not leave a half-written state file. Invalid JSON is preserved as a `.corrupt` backup before defaults are restored.

### File structure

```text
.
├── main.py
├── pyproject.toml
├── uv.lock
├── state.json
├── src/
│   └── quiz_game/
│       ├── app.py
│       ├── data.py
│       ├── game.py
│       ├── input_utils.py
│       ├── quiz.py
│       └── storage.py
└── tests/
    └── test_quiz_game.py
```

### Persistent data

`state.json` is stored at the repository root as required. Its `quizzes` array stores each question, four choices, and the correct answer number. `best_score` stores the highest number of correct answers. The file is UTF-8, and Korean question text is written without ASCII escaping.

Example structure:

```json
{
  "quizzes": [
    {
      "question": "파이썬을 처음 만든 사람은 누구인가요?",
      "choices": ["Linus Torvalds", "Guido van Rossum", "James Gosling", "Bjarne Stroustrup"],
      "answer": 2
    }
  ],
  "best_score": 9
}
```

## Verification

The test suite covers answer checking, invalid quiz data, retrying invalid input, UTF-8 defaults, persistence across reloads, and recovery from corrupt JSON.

```powershell
$env:PYTHONPATH = "src"
uv run --no-sync python -m unittest discover -s tests -v
```

Result: **6 tests passed**.

The application was also run through its console menu. A new question was added, the nine-question list was displayed, all nine questions were answered correctly, and the best score was read back from `state.json`.

```text
📂 퀴즈 9개를 준비했습니다.
📋 등록된 퀴즈 목록 (총 9개)
🏆 결과: 9문제 중 9문제 정답 (100점)
🎉 새로운 최고 점수입니다!
🏆 최고 점수: 9개 정답
STATE quizzes=9 best_score=9
```

## Git workflow

Development was split into feature commits. Quiz play was developed on `feature/quiz-play` (`5898832`) and merged into `main` (`c89a057`). The history contains more than ten meaningful commits after this documentation commit. The clone and pull exercise was performed from the public GitHub repository; the exact commands and resulting commit IDs are recorded below after synchronization.

```powershell
git log --oneline --graph --decorate --all
```

## Screenshots

The mission asks for screenshots of the development environment, menu and play output, and the Git graph. Add the real local captures here:

- `images/environment.png`
- `images/menu-and-play.png`
- `images/git-graph.png`

No example or reference-repository screenshots are used as evidence.

## Recovery behavior

If `state.json` is missing, the default quiz set is written and loaded. If it contains invalid JSON or violates the expected schema, the original file is kept as `state.json.corrupt` (or the next numbered backup), defaults are restored, and the game continues. Disk write errors are reported without terminating the active session unexpectedly.
