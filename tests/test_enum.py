from io import StringIO
from contextlib import redirect_stdout

from src.main import Lang
from tests.tools import run


def test_class():
    test_cases = [
        ("./tests/cases/enum.txt",
         ("False",)),
    ]

    run(test_cases, True, fun_handle_exp=lambda x: "\n".join(x) + "\n")


def main():
    test_class()


if __name__ == '__main__':
    main()
