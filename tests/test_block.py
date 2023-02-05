from io import StringIO
from contextlib import redirect_stdout

from src.main import Lang
from tests.tools import run


def test():
    test_cases = [
        ("var a = 100; a = 200; print(a);",
         "200\n"),
        ("var a = 100; var b = 200; { b= 300;} print(b);",
         "300\n"),
        ("var a = 100; var b = 200; { var b= 255;print(b);} ",
         "255\n"),
    ]

    run(test_cases, False)


def main():
    test()


if __name__ == '__main__':
    main()
