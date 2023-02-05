from io import StringIO
from contextlib import redirect_stdout

from src.main import Lang
from tests.tools import run


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

    run(test_cases, False, code_gen=lambda x: f"print({x});",
        fun_handle_exp=lambda x: str(x) + "\n")


def main():
    test()


if __name__ == '__main__':
    main()
