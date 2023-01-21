from io import StringIO
from contextlib import redirect_stdout

from src.main import Lox


def helper(res: str):
    tmp = res.split()[0]

    try:
        return float(tmp)
    except ValueError as e:
        if tmp == "True":
            return True
        elif tmp == "False":
            return False
        else:
            print(f"res: <{res}> tmp: <{tmp}> : not support")
            exit(-1)


def test():

    test_cases = [
        ("1.0 + 2", 3),
        ("3 *2.0", 6),
        ("2- 3.5", -1.5),
        ("3/4", 0.75),
        ("1+(3/4+1) /  (1+3)", 1.4375),
        ("------1 + (1--3)", 5),
        ("!2", False),
    ]

    lox = Lox()
    for case in test_cases:
        src, expected = case
        with redirect_stdout(StringIO()) as f:
            lox.run(f"print({src});")
        result = f.getvalue()
        assert helper(result) == expected, f"src <{src}> res: <{result}> expect <{expected}>"


def main():
    test()


if __name__ == '__main__':
    main()
