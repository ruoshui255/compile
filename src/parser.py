from src.expr import *
from src.token import TokenType, Token
from src.utils import error_compiler


def report_error(token, msg):
    error_compiler(token, msg)
    return ParseError()


class ParseError(Exception):
    def __init__(self):
        pass


class Parser:
    def __init__(self, tokens: list[Token]):
        self.current = 0
        self.tokens = tokens
        self.error = False

    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.comparison()

        while self.match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = ExprBinary(expr, operator, right)

        return expr

    def comparison(self):
        expr = self.term()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = ExprBinary(expr, operator, right)

        return expr

    def term(self):
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = ExprBinary(expr, operator, right)

        return expr

    def factor(self):
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = ExprBinary(expr, operator, right)

        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return ExprUnary(operator, right)

        return self.primary()

    def primary(self):
        match self.advance().type:
            case TokenType.FALSE:
                return ExprLiteral(False)
            case TokenType.TRUE:
                return ExprLiteral(True)
            case TokenType.NIL:
                return ExprLiteral(None)
            case TokenType.NUMBER | TokenType.STRING:
                return ExprLiteral(self.previous().literal)
            case TokenType.LEFT_PAREN:
                expr = self.expression()
                self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression")
                return ExprGrouping(expr)
            case _:
                raise error_compiler(self.peek(), "Expect expression.")
                # print("undefined token type")

    def parse(self):
        try:
            return self.expression()
        except ParseError as e:
            return

    def consume(self, expected_token_type, msg_error):
        if self.check(expected_token_type):
            return self.advance()
        error_compiler(self.peek(), msg_error)

    def match(self, *types):
        for t in types:
            if self.check(t):
                self.advance()
                return True
        return False

    def check(self, type):
        if self.at_end():
            return False
        return self.peek().type == type

    def advance(self) -> Token:
        if not self.at_end():
            self.current += 1

        return self.previous()

    def at_end(self):
        return self.current == len(self.tokens)

    def peek(self):
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def synchronize(self):
        self.advance()

        while not self.at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return

            if self.peek().type in [
                TokenType.CLASS,
                TokenType.FUN,
                TokenType.VAR,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN,
            ]:
                return

            self.advance()