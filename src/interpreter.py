from src.expr import ExprUnary, ExprLiteral, ExprBinary, ExprGrouping
from src.main import Lox
from src.scanner import TokenType


class RuntimeExcept(RuntimeError):
    def __init__(self, token, msg):
        super.__init__(msg)
        self.token = token


class Interpreter:
    def __init__(self):
        pass

    def interpreter(self, expression):
        try:
            value = self.evaluate(expression)
            print(str(value))
        except RuntimeExcept as e:
            Lox.error_runtime(e)

    @staticmethod
    def visit_literal_expr(expr: ExprLiteral):
        return expr.value

    def visit_grouping_expr(self, expr: ExprGrouping):
        return self.evaluate(expr.expression)

    def evaluate(self, expr):
        return expr.accept(self)

    def visit_unary_expr(self, expr: ExprUnary):
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                self.check_number_operand(expr.operator, right)
                return -right
            case TokenType.BANG:
                return not self.truthy(right)

            case _:
                print(f"not yet implement in unary: {expr.operator}")

    @staticmethod
    def truthy(expr):
        if expr is None:
            return False

        if isinstance(expr, bool):
            return expr

        return True

    def visit_binary_expr(self, expr: ExprBinary):
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
                number = isinstance(left, int) and isinstance(left, float) and isinstance(right, int) and isinstance(right, float)
                string = isinstance(left, str) and isinstance(right, str)
                if number or string:
                    return left + right
                raise RuntimeExcept(expr.operator, "Operands must be two numbers or two strings.")
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
                print(f"not yet implement in binary: {expr.operator}")

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
        raise RuntimeExcept(operator, "Operand must be a number")

    @staticmethod
    def check_number_operands(operator, left, right):
        if isinstance(left, int) or isinstance(left, int):
            return
        if isinstance(right, float) or isinstance(right, float):
            return
        raise RuntimeExcept(operator, "Operand must be a number")

