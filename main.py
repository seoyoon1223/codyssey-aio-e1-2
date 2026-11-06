"""Run the quiz game from the project root."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from quiz_game.app import run


if __name__ == "__main__":
    run()
