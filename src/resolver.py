from enum import Enum, auto
from typing import TYPE_CHECKING

from src.expr import *
from src.statement import *
from src.token import Token
from src.utils import error_compiler
if TYPE_CHECKING:
    from src.interpreter import Interpreter


class FunctionType(Enum):
    NULL = auto()
    Function = auto()
    Initializer = auto()
    Method = auto


class ClassType(Enum):
    NULL = auto()
    Class = auto()
    SubClass = auto()


class Resolver:
    def __init__(self, interpreter: 'Interpreter'):
        self.interpreter = interpreter
        self.scopes: list[dict] = []
        self.class_current: ClassType = ClassType.NULL
        self.function_current: ClassType = FunctionType.NULL

        self.error: bool = False

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
        function_closing = self.function_current
        self.function_current = type

        self.begin_scope()
        for param in function.params:
            self.declare(param)
            self.define(param)

        self.resolve(function.body)
        self.end_scope()

        self.function_current = function_closing

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
        if self.function_current == FunctionType.NULL:
            self.report_error(stmt.keyword, "Can't return from top-level code.")

        if stmt.value is not None:
            if self.function_current == FunctionType.Initializer:
                self.report_error(stmt.keyword, "Can't return a value from an initializer.")
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

    def visit_stmt_class(self, stmt: StmtClass):
        class_enclosing = self.class_current
        self.class_current = ClassType.Class

        self.declare(stmt.name)
        self.define(stmt.name)

        # prevent input case: class Foo < Foo {}
        # That causes a circular reference
        class_name = stmt.name.lexeme
        if (stmt.superclass is not None) and (class_name == stmt.superclass.name.lexeme):
            self.report_error(stmt.superclass.name, "A class can't inherit from itself.")

        if stmt.superclass is not None:
            self.class_current = ClassType.SubClass
            self.resolve(stmt.superclass)

        # super class closure
        if stmt.superclass is not None:
            self.begin_scope()
            scope = self.scopes[-1]
            scope["super"] = True

        self.begin_scope()
        top = self.scopes[-1]
        top["this"] = True

        for method in stmt.methods:
            declaration = FunctionType.Method
            if method.name.lexeme == "init":
                declaration = FunctionType.Initializer

            self.resolve_function(method, declaration)

        self.end_scope()

        if stmt.superclass is not None:
            self.end_scope()

        self.class_current = class_enclosing
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

    def visit_expr_get(self, expr: ExprGet):
        self.resolve(expr.object)
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

    def visit_expr_this(self, expr: ExprThis):
        if self.class_current == ClassType.NULL:
            self.report_error(expr.keyword, "Can't user 'this' outside of a class")
            return None

        self.resolve_local(expr, expr.keyword)
        return None

    def visit_expr_super(self, expr: ExprSuper):
        if self.class_current == ClassType.NULL:
            self.report_error(expr.keyword, "Can't use 'super' outside of a class.")
        elif self.class_current != ClassType.SubClass:
            self.report_error(expr.keyword, "Can't use 'super' in a class with no superclass.")

        self.resolve_local(expr, expr.keyword)
        return None

    def visit_expr_set(self, expr: ExprSet):
        self.resolve(expr.value)
        self.resolve(expr.object)
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

    def report_error(self, t: any, msg: str):
        self.error = True
        error_compiler(t, msg)
