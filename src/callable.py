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
    def __init__(self, declaration: StmtFunction, closure: Environment, initialized: bool):
        super().__init__()
        self.initialized: bool = initialized
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
            if self.initialized:
                return self.closure.get_at(0, "this")
            return e.value

        return None

    def bind(self, instance):
        environment = Environment(self.closure)
        environment.define("this", instance)
        return Function(self.declaration, environment, self.initialized)

    def __str__(self):
        return f"<fun {self.declaration.name.lexeme}>"


class Class(Callable):
    def __init__(self, name: str, methods: dict[str, Function]):
        self.name = name
        self.methods = methods

    def arity(self):
        initializer = self.find_method("init")
        if initializer is None:
            return 0
        else:
            return initializer.arity()

    def call(self, interpreter, arguments):
        instance = Instance(self)

        initializer = self.find_method("init")
        if initializer is not None:
            initializer.bind(instance).call(interpreter, arguments)

        return instance

    def find_method(self, name: str):
        res = self.methods.get(name, None)
        return res

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

        method = self.klass.find_method(name.lexeme)
        if method is not None:
            return method.bind(self)

        raise RuntimeException(name, f"Undefined property '{name.lexeme}'.")

    def __str__(self):
        return f"{self.klass.name} instance"

