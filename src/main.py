import sys

from src.interpreter import Interpreter
from src.parser import Parser
from src.scanner import TokenType, Token, Scanner


class Lox:
    error_compile = False
    error_run = False
    interpreter = Interpreter()

    @staticmethod
    def error_compiler(t, msg):
        match t:
            case int():
                Lox.report(t, "", msg)
            case Token():
                if t.type == TokenType.EOF:
                    Lox.report(t, "at end", msg)
                else:
                    Lox.report(t.type, "at '" + t.lexeme + "'", msg)
            case _:
                print("not yet implement")

    @staticmethod
    def report(line, where, msg):
        print(f"[line {line}] Error {where} : {msg}")
        Lox.error_compile = True

    @staticmethod
    def main():
        if len(sys.argv) < 2:
            Lox.run_prompt()
        elif len(sys.argv) == 2:
            Lox.run_file(sys.argv[1])
        else:
            print("file too more")
            exit(-1)

    @staticmethod
    def run_prompt():
        while True:
            try:
                line = input("> ")
                Lox.run(line)
                Lox.error_compile = False
            except EOFError:
                print("exit")
                exit(-1)

    @staticmethod
    def run_file(filename):
        with open(filename, "r", encoding="utf-8") as f:
            src = f.read()
            Lox.run(src)

        if Lox.error_compile:
            exit(65)
        if Lox.error_run:
            exit(70)

    @staticmethod
    def run(src):
        scanner = Scanner(src)
        tokens = scanner.scan_tokens()

        parser = Parser(tokens)
        expression = parser.parse()

        if Lox.error_compile:
            return

        Lox.interpreter.interpreter(expression)

    @classmethod
    def error_runtime(cls, e):
        print(f"{e} \n [line + {e.token.line}]")
        Lox.error_run = True


def main():
    Lox.main()


if __name__ == '__main__':
    main()
