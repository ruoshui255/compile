from src.token import TokenType, Token


def report(line, where, msg):
    print(f"[line {line}] Error {where} : {msg}")


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
            print("not yet implement")


