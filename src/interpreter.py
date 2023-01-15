from src.expr import ExprUnary, ExprLiteral, ExprBinary, ExprGrouping
from src.token import TokenType


class RuntimeExcept(RuntimeError):
    def __init__(self, token, msg):
        super().__init__(msg)
        self.token = token


class Interpreter:
    def __init__(self):
        self.error = False

    def interpreter(self, expression):
        try:
            value = self.evaluate(expression)
            result = value
            print(result)
            return result
        except RuntimeExcept as e:
            self.error_runtime(e)

    @staticmethod
    def visit_expr_literal(expr: ExprLiteral):
        return expr.value

    def visit_expr_grouping(self, expr: ExprGrouping):
        return self.evaluate(expr.expression)

    def evaluate(self, expr):
        return expr.accept(self)

    def visit_expr_unary(self, expr: ExprUnary):
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
                number = isinstance(left, int) or isinstance(left, float) or isinstance(right, int) or isinstance(right, float)
                string = isinstance(left, str) or isinstance(right, str)
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

    def error_runtime(self, e):
        print(f"{e} \n [line + {e.token.line}]")
        self.error = True

