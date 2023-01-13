class ExprBinary:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_ExprBinary(self)


class ExprGrouping:
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_ExprGrouping(self)


class ExprLiteral:
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_ExprLiteral(self)


class ExprUnary:
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_ExprUnary(self)


