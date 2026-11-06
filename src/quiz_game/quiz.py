"""Quiz data model and answer validation."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Quiz:
    question: str
    choices: tuple[str, str, str, str]
    answer: int

    def __post_init__(self) -> None:
        if not self.question.strip():
            raise ValueError("문제는 비어 있을 수 없습니다")
        if len(self.choices) != 4 or any(not choice.strip() for choice in self.choices):
            raise ValueError("퀴즈에는 내용이 있는 선택지가 네 개 필요합니다")
        if self.answer not in range(1, 5):
            raise ValueError("정답 번호는 1부터 4까지여야 합니다")

    def is_correct(self, answer: int) -> bool:
        return answer == self.answer

    def to_dict(self) -> dict[str, object]:
        return {
            "question": self.question,
            "choices": list(self.choices),
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Quiz":
        choices = data.get("choices")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("저장된 선택지 형식이 올바르지 않습니다")
        return cls(
            question=str(data.get("question", "")),
            choices=tuple(str(choice) for choice in choices),
            answer=int(data.get("answer", 0)),
        )
