"""Default Python and computer fundamentals questions."""

from quiz_game.quiz import Quiz

DEFAULT_QUIZZES = (
    Quiz(
        "파이썬을 처음 만든 사람은 누구인가요?",
        ("Linus Torvalds", "Guido van Rossum", "James Gosling", "Bjarne Stroustrup"),
        2,
    ),
    Quiz(
        "화면에 문자열을 출력하는 파이썬 함수는 무엇인가요?",
        ("input()", "write()", "print()", "show()"),
        3,
    ),
    Quiz(
        "여러 값을 순서대로 담고 변경할 수 있는 자료형은 무엇인가요?",
        ("list", "tuple", "bool", "float"),
        1,
    ),
    Quiz(
        "파이썬의 참·거짓 값으로 올바른 쌍은 무엇인가요?",
        ("YES / NO", "1 / 0", "True / False", "On / Off"),
        3,
    ),
    Quiz(
        "키와 값의 쌍을 저장하는 자료형은 무엇인가요?",
        ("set", "dict", "str", "int"),
        2,
    ),
    Quiz(
        "문자열이나 리스트의 항목 수를 알려주는 함수는 무엇인가요?",
        ("len()", "count()", "size()", "range()"),
        1,
    ),
    Quiz(
        "두 값이 같은지 비교하는 연산자는 무엇인가요?",
        ("=", "!=", ">=", "=="),
        4,
    ),
    Quiz(
        "리스트의 항목을 하나씩 반복할 때 주로 사용하는 문장은 무엇인가요?",
        ("for", "def", "class", "import"),
        1,
    ),
)
