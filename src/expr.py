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


class ExprCall:
    def __init__(self, callee, paren, arguments):
        self.callee = callee
        self.paren = paren
        self.arguments = arguments

    def accept(self, visitor):
        return visitor.visit_expr_call(self)


class ExprGet:
    def __init__(self, object, name):
        self.object = object
        self.name = name

    def accept(self, visitor):
        return visitor.visit_expr_get(self)


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


class ExprLogical:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_expr_logical(self)


class ExprSet:
    def __init__(self, object, name, value):
        self.object = object
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_expr_set(self)


class ExprSuper:
    def __init__(self, keyword, method):
        self.keyword = keyword
        self.method = method

    def accept(self, visitor):
        return visitor.visit_expr_super(self)


class ExprThis:
    def __init__(self, keyword):
        self.keyword = keyword

    def accept(self, visitor):
        return visitor.visit_expr_this(self)


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


