"""Validated console input helpers."""


class GracefulExit(Exception):
    """Raised when the user ends the input stream or presses Ctrl+C."""


def read_text(prompt: str) -> str:
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        raise GracefulExit from None


def read_nonempty(prompt: str) -> str:
    while True:
        value = read_text(prompt).strip()
        if value:
            return value
        print("⚠️ 입력이 비어 있습니다. 다시 입력해 주세요.")


def read_integer(prompt: str, minimum: int, maximum: int) -> int:
    while True:
        value = read_text(prompt).strip()
        if not value:
            print("⚠️ 입력이 비어 있습니다. 다시 입력해 주세요.")
            continue
        try:
            number = int(value)
        except ValueError:
            print("⚠️ 숫자를 입력해 주세요.")
            continue
        if minimum <= number <= maximum:
            return number
        print(f"⚠️ {minimum}부터 {maximum} 사이의 숫자를 입력해 주세요.")
