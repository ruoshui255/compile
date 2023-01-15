from src.main import Lox


def test_add():
    lox = Lox()

    test_cases = [
        ("1.0 + 2", 3),
        ("3 *2.0", 6),
        ("2- 3.5", -1.5),
        ("3/4", 0.75),
        ("1+(3/4+1) /  (1+3)", 1.4375),
        ("------1 + (1--3)", 5),
        ("!2", False),
    ]

    for case in test_cases:
        src, expected = case
        result = lox.run(src)
        assert result == expected, f"src <{src}> res: <{result}> expect <{expected}>"


def main():
    test_add()


if __name__ == '__main__':
    main()
