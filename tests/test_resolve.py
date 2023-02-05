from tests.tools import run


def test():
    test_cases = [
        ("./tests/cases/resolve.txt",
         ("global", "global"))
    ]

    run(test_cases, True, fun_handle_exp=lambda x: "\n".join(x) + "\n")


def main():
    test()


if __name__ == '__main__':
    main()
