from io import StringIO
from contextlib import redirect_stdout

from src.main import Lox


def test_class():
    test_cases = [
        ("./example/class1.lox",
         ("Jane", "Hello", "123")),
        ("./example/class2.lox",
         ("Foo instance", "1", "2", "4", "Foo instance", "nil", "2", "3", "5"))
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
    test_class()


if __name__ == '__main__':
    main()
