class ExprAssign:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_expr_assign(self)


class ExprBinary:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_expr_binary(self)


class ExprGrouping:
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_expr_grouping(self)


class ExprLiteral:
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_expr_literal(self)


class ExprUnary:
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_expr_unary(self)


class ExprVariable:
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_expr_variable(self)


