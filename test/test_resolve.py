from io import StringIO
from contextlib import redirect_stdout

from src.main import Lox


def test():
    test_cases = [
        ("./test/cases/resolve.txt",
         ("global", "global"))
    ]

    lox = Lox()
    for case in test_cases:
        filename, data = case
        with open(filename, "r", encoding="utf-8") as f:
            src = f.read()

        expected = "\n".join(data) + "\n"
        with redirect_stdout(StringIO()) as f:
            lox.run(src)

        result = f.getvalue()
        assert result == expected, f"src <{src}> res: <{result}> expect <{expected}>"


def main():
    test()


if __name__ == '__main__':
    main()
