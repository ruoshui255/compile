import sys

from src.token import TokenType, Token


def log_error(*args, **kwargs):
    print("\033[;33m[Error]\033[;0m", *args, **kwargs, file=sys.stderr)


def report(line, where, msg):
    log_error(f"[line {line}] Error {where} : {msg}")


def error_compiler(t, msg):
    match t:
        case int():
            report(t, "", msg)
        case Token():
            if t.type == TokenType.EOF:
                report(t.line, "at end", msg)
            else:
                report(t.line, "at '" + t.lexeme + "'", msg)
        case _:
            log_error("not yet implement")


def log(*args, **kwargs):
    debug = False
    if debug:
        log_error(*args, **kwargs)
    else:
        pass