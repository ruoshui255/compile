from io import StringIO
from contextlib import redirect_stdout

from src.main import Lox


def test_block():
    test_cases = [
        ("var a = 100; a = 200; print(a);",
         "200.0\n"),
        ("var a = 100; var b = 200; { b= 300;} print(b);",
         "300.0\n"),
        ("var a = 100; var b = 200; { var b= 255;print(b);} ",
         "255.0\n"),
    ]

    lox = Lox()
    for case in test_cases:
        src, expected = case
        with redirect_stdout(StringIO()) as f:
            lox.run(src)

        result = f.getvalue()
        assert result == expected, f"src <{src}> res: <{result}> expect <{expected}>"


def main():
    test_block()


if __name__ == '__main__':
    main()
