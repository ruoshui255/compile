from io import StringIO
from contextlib import redirect_stdout

from src.main import Lox


def test_block():
    test_cases = [
        ("./example/block.lox",
         ("inner a", "outer b", "global c", "outer a", "outer b", "global c", "global a", "global b", "global c")),
        ("./example/closure.lox",
         ("1.0", "2.0")),
        ("./example/return.lox",
         ("0.0", "1.0", "1.0", "2.0", "3.0", "5.0", "8.0", "13.0", "21.0", "34.0", "55.0", "89.0", "144.0", "233.0",
          "377.0", "610.0", "987.0", "1597.0", "2584.0", "4181.0")),
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
    test_block()


if __name__ == '__main__':
    main()
