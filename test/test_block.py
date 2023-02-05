from io import StringIO
from contextlib import redirect_stdout

from src.main import Lang


def test():
    test_cases = [
        ("var a = 100; a = 200; print(a);",
         "200\n"),
        ("var a = 100; var b = 200; { b= 300;} print(b);",
         "300\n"),
        ("var a = 100; var b = 200; { var b= 255;print(b);} ",
         "255\n"),
    ]

    lang = Lang()
    for case in test_cases:
        src, expected = case
        with redirect_stdout(StringIO()) as f:
            lang.run(src)

        result = f.getvalue()
        assert result == expected, f"src <{src}> res: <{result}> expect <{expected}>"


def main():
    test()


if __name__ == '__main__':
    main()
