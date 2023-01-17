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


