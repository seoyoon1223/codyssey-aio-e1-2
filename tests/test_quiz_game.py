"""Unit tests for quiz models, input validation, and persistence."""

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from quiz_game.data import DEFAULT_QUIZZES
from quiz_game.input_utils import read_integer
from quiz_game.quiz import Quiz
from quiz_game.storage import GameState, load_state, save_state


class QuizTests(unittest.TestCase):
    def test_answer_check(self) -> None:
        quiz = DEFAULT_QUIZZES[0]
        self.assertTrue(quiz.is_correct(2))
        self.assertFalse(quiz.is_correct(1))

    def test_invalid_quiz_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Quiz("빈 선택지", ("A", "", "C", "D"), 1)


class InputTests(unittest.TestCase):
    def test_retries_invalid_and_whitespace_input(self) -> None:
        output = io.StringIO()
        with patch("builtins.input", side_effect=["abc", " 9 ", "  ", " 3 "]), patch(
            "sys.stdout", output
        ):
            result = read_integer("선택: ", 1, 5)
        self.assertEqual(result, 3)
        self.assertEqual(output.getvalue().count("⚠️"), 3)


class StorageTests(unittest.TestCase):
    def test_missing_state_uses_defaults_and_writes_utf8_json(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "state.json"
            state = load_state(path, DEFAULT_QUIZZES)
            self.assertEqual(len(state.quizzes), len(DEFAULT_QUIZZES))
            self.assertIsNone(state.best_score)
            saved = json.loads(path.read_text(encoding="utf-8"))
            self.assertIn("파이썬", saved["quizzes"][0]["question"])

    def test_quizzes_and_score_survive_reload(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "state.json"
            state = GameState(list(DEFAULT_QUIZZES), best_score=7)
            state.quizzes.append(Quiz("새 문제", ("A", "B", "C", "D"), 4))
            self.assertTrue(save_state(path, state))
            restored = load_state(path, DEFAULT_QUIZZES)
            self.assertEqual(restored.best_score, 7)
            self.assertEqual(restored.quizzes[-1].question, "새 문제")

    def test_corrupt_file_is_backed_up_and_recovered(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "state.json"
            path.write_text("{invalid", encoding="utf-8")
            with patch("sys.stdout", io.StringIO()):
                restored = load_state(path, DEFAULT_QUIZZES)
            self.assertEqual(len(restored.quizzes), len(DEFAULT_QUIZZES))
            self.assertTrue(path.with_suffix(".json.corrupt").is_file())
            self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["best_score"], None)


if __name__ == "__main__":
    unittest.main()
