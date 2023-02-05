from io import StringIO
from contextlib import redirect_stdout

from src.main import Lang
from tests.tools import run


def test():
    test_cases = [
        ("./tests/cases/block.txt",
         ("inner a", "outer b", "global c", "outer a", "outer b", "global c", "global a", "global b", "global c")),
        ("./tests/cases/closure.txt",
         ("1", "2")),
        ("./tests/cases/return.txt",
         ("0", "1", "1", "2", "3", "5", "8", "13", "21", "34", "55", "89", "144", "233",
          "377", "610", "987", "1597", "2584", "4181")),
    ]

    run(test_cases, True, fun_handle_exp=lambda x: "\n".join(x) + "\n")

def main():
    test()


if __name__ == '__main__':
    main()
