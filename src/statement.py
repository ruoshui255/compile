from src.token import Token


class StmtBlock:
    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_stmt_block(self)


class StmtExpression:
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_stmt_expression(self)


class StmtFunction:
    def __init__(self, name: Token, params, body):
        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor):
        return visitor.visit_stmt_function(self)


class StmtIf:
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor):
        return visitor.visit_stmt_if(self)


class StmtPrint:
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_stmt_print(self)


class StmtVar:
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visit_stmt_var(self)


class StmtWhile:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visit_stmt_while(self)


