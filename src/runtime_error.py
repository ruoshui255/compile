from src.token import Token


class RuntimeException(Exception):
    def __init__(self, token: Token, msg: str):
        super().__init__(msg)
        self.token = token


class Return(RuntimeError):
    def __init__(self, value):
        super().__init__("")
        self.value = value
