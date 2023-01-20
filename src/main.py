import sys

from src.interpreter import Interpreter
from src.parser import Parser
from src.resolver import Resolver
from src.scanner import Scanner
from src.utils import log, log_error


class Lox:
    def __init__(self):
        self.scanner = None
        self.parser = None
        self.interpreter = Interpreter()

    def run_prompt(self):
        while True:
            try:
                line = input("> ")
                self.run(line)
            except EOFError:
                print("exit")
                exit(-1)

    def run_file(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            src = f.read()
            self.run(src)

        if self.scanner.error:
            return
        if self.parser.error:
            exit(65)
        if self.interpreter.error:
            exit(70)

    def run(self, src):
        self.scanner = Scanner(src)
        tokens = self.scanner.scan_tokens()

        if self.scanner.error:
            return

        self.parser = Parser(tokens)
        statements = self.parser.parse()

        log(f"parser error {self.parser.error}")
        if self.parser.error:
            return

        resolver = Resolver(self.interpreter)
        resolver.resolve(statements)
        if resolver.error:
            return

        self.interpreter.interpreter(statements)

    def debug_token(self):
        for t in self.scanner.tokens:
            print("debug", t)


def main():
    lox = Lox()
    if len(sys.argv) < 2:
        lox.run_prompt()
    elif len(sys.argv) == 2:
        lox.run_file(sys.argv[1])
    else:
        log_error("file too more")
        exit(-1)


if __name__ == '__main__':
    main()
