"""UTF-8 JSON persistence for quizzes and the best score."""

import json
import shutil
from dataclasses import dataclass
from pathlib import Path

from quiz_game.quiz import Quiz


@dataclass
class GameState:
    quizzes: list[Quiz]
    best_score: int | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }


def load_state(path: Path, default_quizzes: tuple[Quiz, ...]) -> GameState:
    """Load saved data, backing up invalid JSON and restoring defaults."""
    if not path.exists():
        state = GameState(list(default_quizzes))
        save_state(path, state)
        return state

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or not isinstance(data.get("quizzes"), list):
            raise ValueError("state.json 스키마가 올바르지 않습니다")
        quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
        best_score = data.get("best_score")
        if best_score is not None and (not isinstance(best_score, int) or best_score < 0):
            raise ValueError("최고 점수 형식이 올바르지 않습니다")
        return GameState(quizzes, best_score)
    except (OSError, json.JSONDecodeError, TypeError, ValueError, KeyError) as error:
        print(f"저장 파일을 읽지 못해 기본 데이터로 복구합니다: {error}")
        _backup_corrupt_file(path)
        state = GameState(list(default_quizzes))
        save_state(path, state)
        return state


def save_state(path: Path, state: GameState) -> bool:
    """Write a complete state atomically as UTF-8 JSON."""
    temporary_path = path.with_suffix(f"{path.suffix}.tmp")
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path.write_text(
            json.dumps(state.to_dict(), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        temporary_path.replace(path)
        return True
    except OSError as error:
        print(f"저장에 실패했습니다: {error}")
        try:
            temporary_path.unlink(missing_ok=True)
        except OSError:
            pass
        return False


def _backup_corrupt_file(path: Path) -> None:
    if not path.exists():
        return
    backup = path.with_suffix(f"{path.suffix}.corrupt")
    suffix = 1
    while backup.exists():
        backup = path.with_suffix(f"{path.suffix}.corrupt.{suffix}")
        suffix += 1
    try:
        shutil.copy2(path, backup)
    except OSError:
        print("손상 파일 백업에 실패했습니다. 기본 데이터로 계속합니다.")
