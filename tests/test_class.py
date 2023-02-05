from io import StringIO
from contextlib import redirect_stdout

from src.main import Lang
from tests.tools import run


def test_class():
    test_cases = [
        ("./tests/cases/class1.txt",
         ("Jane", "Hello", "123")),
        ("./tests/cases/class2.txt",
         ("Foo instance", "1", "2", "4", "Foo instance", "nil", "2", "3", "5")),
        ("./tests/cases/class3.txt",
         ("parent method", "child method")),
        ("./tests/cases/class4.txt",
         ("A method",)),
        ("./tests/cases/class5.txt",
         ("[line 3] Error at 'super' : Can't use 'super' in a class with no superclass.",
          "[line 9] Error at 'super' : Can't use 'super' outside of a class."))
    ]

    run(test_cases, True, fun_handle_exp=lambda x: "\n".join(x) + "\n")


def main():
    test_class()


if __name__ == '__main__':
    main()
