import sys
from src.interpreter import Interpreter
from src.parser import Parser
from src.scanner import Scanner


class Lox:
    def __init__(self):
        self.scanner = None
        self.parser = None
        self.interpreter = None

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
        expression = self.parser.parse()

        if self.parser.error:
            return

        self.interpreter = Interpreter()
        return self.interpreter.interpreter(expression)

    def debug_token(self):
        for t in self.scanner.tokens:
            print(t)

def main():
    lox = Lox()
    if len(sys.argv) < 2:
        lox.run_prompt()
    elif len(sys.argv) == 2:
        lox.run_file(sys.argv[0])
    else:
        print("file too more")
        exit(-1)


if __name__ == '__main__':
    main()
