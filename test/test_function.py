from io import StringIO
from contextlib import redirect_stdout

from src.main import Lox


def test():
    test_cases = [
        ("./test/cases/block.txt",
         ("inner a", "outer b", "global c", "outer a", "outer b", "global c", "global a", "global b", "global c")),
        ("./test/cases/closure.txt",
         ("1", "2")),
        ("./test/cases/return.txt",
         ("0", "1", "1", "2", "3", "5", "8", "13", "21", "34", "55", "89", "144", "233",
          "377", "610", "987", "1597", "2584", "4181")),
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
