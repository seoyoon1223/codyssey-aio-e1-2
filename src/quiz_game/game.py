"""Quiz game controller and console menu."""

from pathlib import Path

from quiz_game.data import DEFAULT_QUIZZES
from quiz_game.input_utils import GracefulExit, read_integer
from quiz_game.storage import GameState, load_state, save_state


class QuizGame:
    def __init__(self, state_path: Path) -> None:
        self.state_path = state_path
        self.state: GameState = load_state(state_path, DEFAULT_QUIZZES)

    def run(self) -> None:
        print(f"📂 퀴즈 {len(self.state.quizzes)}개를 준비했습니다.")
        try:
            while True:
                self.show_menu()
                choice = read_integer("선택: ", 1, 5)
                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.show_quizzes()
                elif choice == 4:
                    self.show_score()
                else:
                    self.save()
                    print("게임을 종료합니다.")
                    return
        except GracefulExit:
            print("\n입력이 종료되어 안전하게 저장하고 게임을 마칩니다.")
            self.save()

    @staticmethod
    def show_menu() -> None:
        print(
            "\n========================================\n"
            "        🎯 나만의 파이썬 퀴즈 🎯\n"
            "========================================\n"
            "1. 퀴즈 풀기\n"
            "2. 퀴즈 추가\n"
            "3. 퀴즈 목록\n"
            "4. 최고 점수 확인\n"
            "5. 종료\n"
            "========================================"
        )

    def play_quiz(self) -> None:
        if not self.state.quizzes:
            print("등록된 퀴즈가 없어 시작할 수 없습니다.")
            return
        print(f"\n📝 퀴즈를 시작합니다! (총 {len(self.state.quizzes)}문제)")
        correct_count = 0
        for index, quiz in enumerate(self.state.quizzes, start=1):
            print(f"\n[문제 {index}] {quiz.question}")
            for choice_index, choice in enumerate(quiz.choices, start=1):
                print(f"{choice_index}. {choice}")
            answer = read_integer("정답 번호 (1-4): ", 1, 4)
            if quiz.is_correct(answer):
                correct_count += 1
                print("✅ 정답입니다!")
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")
        print(
            f"\n🏆 결과: {len(self.state.quizzes)}문제 중 "
            f"{correct_count}문제 정답 ({correct_count * 100 // len(self.state.quizzes)}점)"
        )

    def add_quiz(self) -> None:
        print("퀴즈 추가 기능을 다음 단계에서 연결합니다.")

    def show_quizzes(self) -> None:
        if not self.state.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.state.quizzes)}개)")
        for index, quiz in enumerate(self.state.quizzes, start=1):
            print(f"[{index}] {quiz.question}")

    def show_score(self) -> None:
        if self.state.best_score is None:
            print("아직 퀴즈를 풀지 않았습니다.")
            return
        print(f"🏆 최고 점수: {self.state.best_score}개 정답")

    def save(self) -> None:
        save_state(self.state_path, self.state)
