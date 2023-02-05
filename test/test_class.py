from io import StringIO
from contextlib import redirect_stdout

from src.main import Lang


def test_class():
    test_cases = [
        ("./test/cases/class1.txt",
         ("Jane", "Hello", "123")),
        ("./test/cases/class2.txt",
         ("Foo instance", "1", "2", "4", "Foo instance", "nil", "2", "3", "5")),
        ("./test/cases/class3.txt",
         ("parent method", "child method")),
        ("./test/cases/class4.txt",
         ("A method",)),
        ("./test/cases/class5.txt",
         ("[line 3] Error at 'super' : Can't use 'super' in a class with no superclass.",
          "[line 9] Error at 'super' : Can't use 'super' outside of a class."))
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
