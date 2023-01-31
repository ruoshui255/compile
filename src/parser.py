import sys

from src.expr import *
from src.statement import *
from src.token import TokenType, Token
from src.utils import error_compiler, log_error, log


class ParseError(Exception):
    def __init__(self):
        pass


class Parser:
    def __init__(self, tokens: list[Token]):
        self.current = 0
        self.tokens = tokens
        self.error = False

    def expression(self):
        return self.assignment()

    def declaration(self):
        try:
            if self.match(TokenType.CLASS):
                return self.class_declaration()
            if self.match(TokenType.FUN):
                return self.function_statement("function")
            elif self.match(TokenType.VAR):
                return self.var_declaration()
            else:
                return self.statement()
        except ParseError as e:
            self.synchronize()
            log("After Synchronize:", self.peek())

    def class_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect class name.")

        # deal with superclass
        superclass = None
        if self.match(TokenType.LESS):
            self.consume(TokenType.IDENTIFIER, "Expect superclass name.")
            superclass = ExprVariable(self.previous())

        self.consume(TokenType.LEFT_BRACE, "Expect '{' before class body.")

        methods : list[StmtFunction] = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.at_end():
            methods.append(self.function_statement("method"))

        self.consume(TokenType.RIGHT_BRACE, "Expect '}' before class body.")

        return StmtClass(name, superclass, methods)

    def var_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")

        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return StmtVar(name, initializer)

    def statement(self):
        if self.match(TokenType.FOR):
            return self.for_statement()

        if self.match(TokenType.IF):
            return self.if_statement()

        if self.match(TokenType.PRINT):
            return self.print_statement()

        if self.match(TokenType.RETURN):
            return self.return_statement()

        if self.match(TokenType.WHILE):
            return self.while_statement()

        if self.match(TokenType.LEFT_BRACE):
            return StmtBlock(self.block())

        return self.expression_statement()

    def for_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after for.")

        if self.match(TokenType.SEMICOLON):
            initializer = None
        elif self.match(TokenType.VAR):
            initializer = self.var_declaration()
        else:
            initializer = self.expression_statement()

        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

        increment = None
        if not self.check(TokenType.RIGHT_PAREN):
            increment = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after while condition.")

        body = self.statement()

        # { initializer
        #         while(condition) { {body}
        #     increment } }
        if increment is not None:
            body = StmtBlock([body, increment])

        if condition is None:
            condition = ExprLiteral(True)
        body = StmtWhile(condition, body)

        if initializer is not None:
            body = StmtBlock([initializer, body])

        return body

    def while_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after while.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect '(' after while condition.")

        body = self.statement()
        return StmtWhile(condition, body)

    def if_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after if.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        then_statement = self.statement()
        else_statement = None

        if self.match(TokenType.ELSE):
            else_statement = self.statement()

        return StmtIf(condition, then_statement, else_statement)

    def return_statement(self):
        keyword = self.previous()
        value = None

        if not self.check(TokenType.SEMICOLON):
            value = self.expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after return value.")
        return StmtReturn(keyword, value)

    def print_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' before print")
        value = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after print")
        self.consume(TokenType.SEMICOLON, "Expect ';' after print expression")
        return StmtPrint(value)

    def function_statement(self, kind: str):
        name = self.consume(TokenType.IDENTIFIER, f"Expect {kind} name.")
        self.consume(TokenType.LEFT_PAREN, f"Expect '(' after {kind} name.")

        parameters = []
        if not self.check(TokenType.RIGHT_PAREN):
            if len(parameters) >= 255:
                self.report_error(self.peek(), "Can't have more than 255 parameters.")
            parameters.append(self.consume(TokenType.IDENTIFIER, "Expect parameter name."))

            while self.match(TokenType.COMMA):
                if len(parameters) >= 255:
                    self.report_error(self.peek(), "Can't have more than 255 parameters.")
                parameters.append(self.consume(TokenType.IDENTIFIER, "Expect parameter name."))

        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")

        self.consume(TokenType.LEFT_BRACE, "Expect '{' before " + kind + " body.")
        body = self.block()
        return StmtFunction(name, parameters, body)

    def expression_statement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value")
        return StmtExpression(expr)

    def block(self):
        statements = []

        while (not self.check(TokenType.RIGHT_BRACE)) and (not self.at_end()):
            statements.append(self.declaration())

        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def binary_or(self):
        expr = self.binary_and()

        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.binary_and()
            expr = ExprLogical(expr, operator, right)
        return expr

    def binary_and(self):
        expr = self.equality()

        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.binary_and()
            expr = ExprLogical(expr, operator, right)
        return expr

    def assignment(self):
        expr = self.binary_or()

        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, ExprVariable):
                name: Token = expr.name
                return ExprAssign(name, value)
            elif isinstance(expr, ExprGet):
                # expr_get have a higher priority than expr_set,
                # so we convert to expr_set
                return ExprSet(expr.object, expr.name, value)

            self.report_error(equals, "Invalid assignment target.")

        return expr

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

        # https://blog.csdn.net/sgzwiz/article/details/7426448
        # 右结合
        # if self.match(TokenType.MINUS, TokenType.PLUS):
        #     operator = self.previous()
        #     right = self.term()
        #     expr = ExprBinary(expr, operator, right)

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

        return self.call()

    def call(self):
        expr = self.primary()

        while True:
            if self.match(TokenType.LEFT_PAREN):
                expr = self.finish_call(expr)
            elif self.match(TokenType.DOT):
                name = self.consume(TokenType.IDENTIFIER, "Expect property name after '.'.")
                expr = ExprGet(expr, name)
            else:
                break
        return expr

    def finish_call(self, callee):
        arguments = []

        if not self.check(TokenType.RIGHT_PAREN):
            arguments.append(self.expression())
            while self.match(TokenType.COMMA):
                # limit function arguments number
                if len(arguments) >= 255:
                    self.report_error(self.peek(), "Can't have more than 255 arguments.")

                arguments.append(self.expression())

        paren = self.consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")

        return ExprCall(callee, paren, arguments)

    def primary(self):
        t = self.advance()
        match t.type:
            case TokenType.FALSE:
                return ExprLiteral(False)
            case TokenType.TRUE:
                return ExprLiteral(True)
            case TokenType.THIS:
                return ExprThis(self.previous())
            case TokenType.NIL:
                return ExprLiteral(None)
            case TokenType.NUMBER | TokenType.STRING:
                return ExprLiteral(self.previous().literal)
            case TokenType.SUPER:
                keyword = self.previous()
                self.consume(TokenType.DOT, "Expect '.' after 'super'.")
                method = self.consume(TokenType.IDENTIFIER, "Expect superclass method name.")
                return ExprSuper(keyword, method)
            case TokenType.LEFT_PAREN:
                expr = self.expression()
                self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression")
                return ExprGrouping(expr)
            case TokenType.IDENTIFIER:
                return ExprVariable(self.previous())
            case _:
                raise self.report_error(self.peek(), "Expect expression.")
                # print("undefined token type")

    def parse(self):
        statements = []
        while not self.at_end():
            statements.append(self.declaration())

        return statements

    def consume(self, expected_token_type, msg_error):
        if self.check(expected_token_type):
            return self.advance()
        raise self.report_error(self.peek(), msg_error)

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
        return self.current == len(self.tokens) - 1

    def peek(self):
        # print(f"debug: cur {self.current}, len {len(self.tokens)}")
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def report_error(self, token, msg):
        self.error = True
        error_compiler(token, msg)
        return ParseError()

    def synchronize(self):
        self.advance()

        while not self.at_end():
            log("synchronize:", self.previous())
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
