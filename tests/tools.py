from contextlib import redirect_stdout
from io import StringIO

from src.main import Lang


def get_src(data, is_file):
    if not is_file:
        return data

    with open(data, "r", encoding="utf-8") as f:
        src = f.read()
    return src


def run(test_cases: list[set], is_file=False, code_gen=lambda x: x,
        fun_handle_res=lambda x: x, fun_handle_exp=lambda x: x):

    lang = Lang()
    for case in test_cases:
        src, exp = case

        code = code_gen(get_src(src, is_file))
        with redirect_stdout(StringIO()) as f:
            lang.run(code)

        result = fun_handle_res(f.getvalue())
        expected = fun_handle_exp(exp)

        assert result == expected, f"src <{code}> \n" \
                                   f"res: <{repr(result)}> \n" \
                                   f"expect <{repr(expected)}>"
