from src.callable import Callable, Clock, Function, Class, Instance
from src.environment import Environment
from src.expr import *
from src.runtime_error import RuntimeException, Return
from src.statement import *
from src.token import TokenType, Token
from src.utils import log, log_error


class Interpreter:
    def __init__(self):
        self.error = False
        self.globals = Environment()
        self.locals = {}
        self.environment = self.globals

        self.globals.define("clock", Clock())

    def interpreter(self, statements):
        try:
            for stmt in statements:
                self.execute(stmt)
            # value = self.evaluate(expression)
            # result = value
            # print(result)
            # return result
        except RuntimeException as e:
            self.report_error(e)

    # statement execute
    def execute(self, stmt):
        stmt.accept(self)

    def resolve(self, expr, depth: int):
        self.locals[expr] = depth

    def execute_block(self, statements, environment: Environment):
        previous = self.environment
        try:
            self.environment = environment

            for stmt in statements:
                self.execute(stmt)
        finally:
            self.environment = previous

    def visit_stmt_class(self, stmt: StmtClass):
        self.environment.define(stmt.name.lexeme, None)

        methods = {}
        for method in stmt.methods:
            function = Function(method, self.environment)
            methods[method.name.lexeme] = function

        klass = Class(stmt.name.lexeme, methods)
        self.environment.assign(stmt.name, klass)
        return None

    def visit_stmt_block(self, stmt: StmtBlock):
        self.execute_block(stmt.statements, Environment(self.environment))
        return

    def visit_stmt_if(self, stmt: StmtIf):
        if self.truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)

        return

    def visit_stmt_function(self, stmt: StmtFunction):
        function = Function(stmt, self.environment)
        self.environment.define(stmt.name.lexeme, function)
        return None

    def visit_stmt_expression(self, stmt):
        self.evaluate(stmt.expression)

    def visit_stmt_return(self, stmt: StmtReturn):
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)

        raise Return(value)

    def visit_stmt_print(self, stmt):
        value = self.evaluate(stmt.expression)
        print(self.to_string(value))

    def visit_stmt_while(self, stmt: StmtWhile):
        while self.truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)

    def visit_stmt_var(self, stmt):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)

        self.environment.define(stmt.name.lexeme, value)

    # expression
    def evaluate(self, expr):
        return expr.accept(self)

    @staticmethod
    def visit_expr_literal(expr: ExprLiteral):
        return expr.value

    def visit_expr_grouping(self, expr: ExprGrouping):
        return self.evaluate(expr.expression)

    def visit_expr_assign(self, expr: ExprAssign):
        value = self.evaluate(expr.value)
        distance = self.locals.get(expr, None)
        if distance is not None:
            self.environment.assign_at(distance, expr.name, value)
        else:
            self.globals.assign(expr.name, value)
        log("visit expr assign {}".format(value))
        return value

    def visit_expr_unary(self, expr: ExprUnary):
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                self.check_number_operand(expr.operator, right)
                return -right
            case TokenType.BANG:
                return not self.truthy(right)

            case _:
                log_error(f"not yet implement in unary: {expr.operator}")

    def visit_expr_variable(self, expr: ExprVariable):
        return self.lookup_variable(expr.name, expr)

    def visit_expr_this(self, expr: ExprThis):
        return self.lookup_variable(expr.keyword, expr)
        pass

    def visit_expr_set(self, expr: ExprSet):
        obj = self.evaluate(expr.object)

        if not isinstance(obj, Instance):
            raise RuntimeException(expr.name, "Only instances have fields.")

        value = self.evaluate(expr.value)
        obj.set(expr.name, value)
        return value

    def visit_expr_logical(self, expr: ExprLogical):
        left = self.evaluate(expr.left)

        if expr.operator.type == TokenType.OR:
            if self.truthy(left):
                return left
            else:
                return self.evaluate(expr.right)
        elif expr.operator.type == TokenType.AND:
            if not self.truthy(left):
                return left
            else:
                return self.evaluate(expr.right)
        else:
            log_error("Error operator:", expr.operator)

    # visit object properties
    def visit_expr_get(self, expr: ExprGet):
        obj = self.evaluate(expr.object)
        if isinstance(obj, Instance):
            return obj.get(expr.name)

        raise RuntimeException(expr.name, "Only instances have properties.")

    def visit_expr_call(self, expr: ExprCall):
        callee = self.evaluate(expr.callee)

        arguments = []
        for arg in expr.arguments:
            arguments.append(self.evaluate(arg))

        if not isinstance(callee, Callable):
            raise RuntimeException(expr.paren, "Can only call functions and classes.")

        function: Callable = callee
        if len(arguments) != function.arity():
            raise RuntimeException(expr.paren,
                                   "Expected " + function.arity() + " arguments but got " + len(arguments) + ".")

        return function.call(self, arguments)

    def visit_expr_binary(self, expr: ExprBinary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                self.check_number_operands(expr.operator, left, right)
                return left - right
            case TokenType.SLASH:
                self.check_number_operands(expr.operator, left, right)
                return left / right
            case TokenType.STAR:
                self.check_number_operands(expr.operator, left, right)
                return left * right
            case TokenType.PLUS:
                number = isinstance(left, int) or isinstance(left, float) or isinstance(right, int) or isinstance(right,
                                                                                                                  float)
                string = isinstance(left, str) or isinstance(right, str)
                if number or string:
                    return left + right
                raise RuntimeException(expr.operator, "Operands must be two numbers or two strings.")
            case TokenType.GREATER:
                self.check_number_operands(expr.operator, left, right)
                return left > right
            case TokenType.GREATER_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return left >= right
            case TokenType.LESS:
                self.check_number_operands(expr.operator, left, right)
                return left < right
            case TokenType.LESS_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return left <= right
            case TokenType.BANG_EQUAL:
                return not self.equal(left, right)
            case TokenType.BANG:
                return self.equal(left, right)
            case _:
                log_error(f"not yet implement in binary: {expr.operator}")

    @staticmethod
    def truthy(expr):
        if expr is None:
            return False

        if isinstance(expr, bool):
            return expr

        return True

    @staticmethod
    def equal(a, b):
        if a is None and b is None:
            return True
        if a is None:
            return False

        return a == b

    @staticmethod
    def check_number_operand(operator, operand):
        if isinstance(operand, int) or isinstance(operand, float):
            return
        raise RuntimeException(operator, "Operand must be a number")

    @staticmethod
    def check_number_operands(operator, left, right):
        if isinstance(left, int) or isinstance(left, int):
            return
        if isinstance(right, float) or isinstance(right, float):
            return
        raise RuntimeException(operator, "Operand must be a number")

    def report_error(self, e):
        log_error(f"[line {e.token.line}] {e} ")
        self.error = True

    @staticmethod
    def to_string(value):
        if value is None:
            return "nil"
        else:
            return str(value)

    def lookup_variable(self, name: Token, expr):
        distance = self.locals.get(expr, None)
        if distance is not None:
            return self.environment.get_at(distance, name.lexeme)
        else:
            return self.globals.get(name)

        pass
