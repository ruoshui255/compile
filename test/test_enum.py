from io import StringIO
from contextlib import redirect_stdout

from src.main import Lang


def test_class():
    test_cases = [
        ("./test/cases/enum.txt",
         ("False",)),
    ]

    lang = Lang()
    for case in test_cases:
        filename, data = case
        with open(filename, "r", encoding="utf-8") as f:
            src = f.read()

        expected = "\n".join(data) + "\n"
        with redirect_stdout(StringIO()) as f:
            lang.run(src)

        result = f.getvalue()
        assert result == expected, f"src <{src}> res: <{result}> expect <{expected}>"


def main():
    test_class()


if __name__ == '__main__':
    main()
