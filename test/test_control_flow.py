from io import StringIO
from contextlib import redirect_stdout

from src.main import Lox


def test_control_flow():

    test_cases = [
        ("var a = 100; if(a){print(a);} else print(123);",
         "100.0\n"),
        ("var a = 100; if(nil){print(a);} else print(123);",
         "123.0\n"),
        ("var a = 200; var b = 0; for(var a = 1; a < 11; a = a+1){ b = b+a;} print(b); print(a); ",
         "55.0\n200.0\n"),
    ]

    lox = Lox()
    for case in test_cases:
        src, expected = case
        with redirect_stdout(StringIO()) as f:
            lox.run(src)
        result = f.getvalue()
        assert result == expected, f"src <{src}> res: <{result}> expect <{expected}>"


def main():
    test_control_flow()


if __name__ == '__main__':
    main()
