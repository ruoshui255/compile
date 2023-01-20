import time

from src.environment import Environment
from src.runtime_error import Return, RuntimeException
from src.statement import StmtFunction
from src.token import Token


class Callable:

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
    def __init__(self, declaration: StmtFunction, closure: Environment):
        super().__init__()
        self.declaration = declaration
        self.closure = closure

    def arity(self):
        return len(self.declaration.params)

    def call(self, interpreter, arguments):
        environment = Environment(self.closure)
        for index, arg in enumerate(self.declaration.params):
            environment.define(arg.lexeme, arguments[index])

        try:
            interpreter.execute_block(self.declaration.body, environment)
        except Return as e:
            return e.value

        return None

    def __str__(self):
        return f"<fun {self.declaration.name.lexeme}>"


class Class(Callable):
    def __init__(self, name: str):
        self.name = name

    def arity(self):
        return 0

    def call(self, interpreter, arguments):
        instance = Instance(self)
        return instance

    def __str__(self):
        return self.name


class Instance:
    def __init__(self, klass: Class):
        self.klass = klass
        self.fields = {}

    def set(self, name: Token, value):
        self.fields[name.lexeme] = value

    def get(self, name: Token):
        if name.lexeme in self.fields:
            return self.fields.get(name.lexeme)

        raise RuntimeException(name, f"Undefined property '{name.lexeme}'.")

    def __str__(self):
        return f"{self.klass.name} instance"

