import time

from src.environment import Environment
from src.statement import StmtFunction


class Callable:
    def __init__(self):
        pass

    def arity(self):
        pass

    def call(self, interpreter, arguments):
        pass


class Clock(Callable):

    def arity(self):
        return 0

    def call(self, interpreter, arguments):
        return float(time.time() / 1000.0)

    def __str__(self):
        return "<native fun : clock>"


class Function(Callable):
    def __init__(self, declaration: StmtFunction):
        super().__init__()
        self.declaration = declaration

    def arity(self):
        return len(self.declaration.params)

    def call(self, interpreter, arguments):
        environment = Environment(interpreter.globals)
        for index, arg in enumerate(self.declaration.params):
            environment.define(arg.lexeme, arguments[index])

        interpreter.execute_block(self.declaration.body, environment)
        return None

    def __str__(self):
        return f"<fun {self.declaration.name.lexeme}>"
