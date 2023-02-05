from io import StringIO
from contextlib import redirect_stdout

from src.main import Lang


def test():

    test_cases = [
        ("1.0 + 2", 3),
        ("3 *2.0", 6),
        ("2- 3.5", -1.5),
        ("3/4", 0.75),
        ("1+(3/4+1) /  (1+3)", 1.4375),
        ("------1 + (1--3)", 5),
        ("!2", False),
        ('1+"123"', "[line 1] Operands must be two numbers or two strings.")

    ]

    lang = Lang()
    for case in test_cases:
        src, expected = case
        with redirect_stdout(StringIO()) as f:
            lang.run(f"print({src});")
        result = f.getvalue()
        t = str(expected) + "\n"

        assert result == t, f"src <{repr(src)}>\nres <{repr(result)}>\nexp <{repr(expected)}>"


def main():
    test()


if __name__ == '__main__':
    main()
