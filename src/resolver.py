from enum import Enum, auto

from src.expr import *
from src.statement import *
from src.token import Token
from src.utils import error_compiler


class FunctionType(Enum):
    NULL = auto()
    Function = auto()


class Resolver:
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.scopes: list[dict] = []
        self.current_function = FunctionType.NULL

        self.error = False

    # t may be stmts or stmt or expr, but python doesn't care
    def resolve(self, t):
        if isinstance(t, list):
            for stmt in t:
                stmt.accept(self)
        else:
            # t is stmt or expr
            t.accept(self)

    def resolve_local(self, expr, name: Token):
        for i in range(len(self.scopes) - 1, -1, -1):
            scope = self.scopes[i]
            if name.lexeme in scope.keys():
                self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
                return

    def resolve_function(self, function: StmtFunction, type: FunctionType):
        closing_function = self.current_function
        self.current_function = type

        self.begin_scope()
        for param in function.params:
            self.declare(param)
            self.define(param)

        self.resolve(function.body)
        self.end_scope()

        self.current_function = closing_function

    def visit_stmt_expression(self, stmt: StmtExpression):
        self.resolve(stmt.expression)
        return None

    def visit_stmt_if(self, stmt: StmtIf):
        self.resolve(stmt.condition)
        self.resolve(stmt.then_branch)

        if stmt.else_branch is not None:
            self.resolve(stmt.else_branch)

        return None

    def visit_stmt_print(self, stmt: StmtPrint):
        self.resolve(stmt.expression)
        return None

    def visit_stmt_return(self, stmt: StmtReturn):
        if self.current_function == FunctionType.NULL:
            self.report_error(stmt.keyword, "Can't return from top-level code.")

        if stmt.value is not None:
            self.resolve(stmt.value)
        return None

    def visit_stmt_while(self, stmt: StmtWhile):
        self.resolve(stmt.condition)
        self.resolve(stmt.body)
        return None

    def visit_stmt_var(self, stmt: StmtVar):
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self.resolve(stmt.initializer)

        self.define(stmt.name)
        return None

    def visit_stmt_block(self, stmt: StmtBlock):
        self.begin_scope()
        self.resolve(stmt.statements)
        self.end_scope()

        return None

    def visit_stmt_function(self, stmt: StmtFunction):
        self.declare(stmt.name)
        self.define(stmt.name)

        self.resolve_function(stmt, FunctionType.Function)
        return None

    def visit_expr_assign(self, expr: ExprAssign):
        self.resolve(expr.value)
        self.resolve_local(expr, expr.name)
        return None

    def visit_expr_binary(self, expr: ExprBinary):
        self.resolve(expr.left)
        self.resolve(expr.right)
        return None

    def visit_expr_call(self, expr: ExprCall):
        self.resolve(expr.callee)

        for arg in expr.arguments:
            self.resolve(arg)

        return None

    def visit_expr_grouping(self, expr: ExprGrouping):
        self.resolve(expr.expression)
        return None

    def visit_expr_literal(self, expr: ExprLiteral):
        return None

    def visit_expr_logical(self, expr: ExprLogical):
        self.resolve(expr.left)
        self.resolve(expr.right)
        return None

    def visit_expr_unary(self, expr: ExprUnary):
        self.resolve(expr.right)
        return None

    def visit_expr_variable(self, expr: ExprVariable):
        if len(self.scopes) != 0 and self.scopes[-1].get(expr.name.lexeme) == False:
            self.report_error(expr.name, "Can't read local variable in its own initializer.")

        self.resolve_local(expr, expr.name)
        return None

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    def declare(self, name: Token):
        if len(self.scopes) == 0:
            return

        scope = self.scopes[-1]
        if name.lexeme in scope:
            self.report_error(name, "Already a variable with this name in this scope.")
        scope[name.lexeme] = False

    def define(self, name: Token):
        if len(self.scopes) == 0:
            return

        scope = self.scopes[-1]
        scope[name.lexeme] = True

    def report_error(self, t, msg):
        self.error = True
        error_compiler(t, msg)
