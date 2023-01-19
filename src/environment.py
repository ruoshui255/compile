from src.runtime_error import RuntimeException
from src.token import Token
from src.utils import log


class Environment:
    def __init__(self, enclosing=None):
        self.enclosing: Environment = enclosing
        self.values = {}

    def define(self, name: str, value):
        log(f"environment define {name} {value}")
        self.values[name] = value

    def get(self, token: Token):
        name = token.lexeme
        if name in self.values.keys():
            return self.values.get(name)

        if self.enclosing is not None:
            return self.enclosing.get(token)

        raise RuntimeException(token, "Undefined variable '" + name + "'.")

    def assign(self, token: Token, value):
        name = token.lexeme
        if name in self.values.keys():
            self.values[name] = value
            return

        if self.enclosing is not None:
            self.enclosing.assign(token, value)
            return

        raise RuntimeException(token, "Undefined variable '" + name + "'.")
