"""Application entry point for the quiz game."""

from pathlib import Path

from quiz_game.game import QuizGame


def run() -> None:
    QuizGame(Path.cwd() / "state.json").run()
