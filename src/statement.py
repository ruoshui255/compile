class StmtEnum:
    def __init__(self, bodies):
        self.bodies = bodies

    def accept(self, visitor):
        return visitor.visit_stmt_enum(self)


class StmtBlock:
    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_stmt_block(self)


class StmtClass:
    def __init__(self, name, superclass, methods):
        self.name = name
        self.superclass = superclass
        self.methods = methods

    def accept(self, visitor):
        return visitor.visit_stmt_class(self)


class StmtExpression:
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_stmt_expression(self)


class StmtFunction:
    def __init__(self, name, params, body):
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


class StmtReturn:
    def __init__(self, keyword, value):
        self.keyword = keyword
        self.value = value

    def accept(self, visitor):
        return visitor.visit_stmt_return(self)


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


class StmtBreak:
    def __init__(self, t):
        self.token = t

    def accept(self, visitor):
        return visitor.visit_stmt_break(self)


class StmtFor:
    def __init__(self, condition, increment, body):
        self.condition = condition
        self.increment = increment
        self.body = body

    def accept(self, visitor):
        return visitor.visit_stmt_for(self)


class StmtContinue:
    def __init__(self, t):
        self.token = t

    def accept(self, visitor):
        return visitor.visit_stmt_continue(self)
