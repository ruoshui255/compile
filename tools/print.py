import sys


def define_AST(output_folder, filename, types: list[str]):
    """
    types: ["ExprBinary: left, operator, right"]
    """
    file = output_folder + "/" + filename
    with open(file, "w+", encoding="utf-8") as f:
        for type in types:
            class_name = type.split(":")[0].strip()
            args = type.split(":")[1].strip()
            define_type(f, class_name, args)
            f.write("\n\n")


def define_type(f, class_name, fields):
    t = "".join(class_name.split())
    f.write("class " + t + ":\n")
    f.write("    def __init__(self, {}):\n".format(fields))

    for field in fields.split(", "):
        f.write("        self.{0} = {0}\n".format(field))

    f.write("\n")
    f.write("    def accept(self, visitor):\n")

    args = class_name.split()
    temp = "_".join([t.lower() for t in args])
    template = "        return visitor.visit_{}(self)\n"
    ret = template.format(temp)
    f.write(ret)


def main():
    if len(sys.argv) < 1:
        print("Usage: input <output folder>")
        exit(-1)

    output_folder = "."
    define_AST(output_folder, "src/expr.py", [
        "Expr Assign   : name, value",
        "Expr Binary   : left, operator, right",
        "Expr Call     : callee, paren, arguments",
        "Expr Get      : object, name",
        "Expr Grouping : expression",
        "Expr Literal  : value",
        "Expr Logical  : left, operator, right",
        "Expr Set      : object, name, value",
        "Expr Unary    : operator, right",
        "Expr Variable : name"
    ])

    define_AST(output_folder, "src/statement.py", [
        "Stmt Block      : statements",
        "Stmt Class      : name, methods",
        "Stmt Expression : expression",
        "Stmt Function   : name, params, body",
        "Stmt If         : condition, then_branch, else_branch",
        "Stmt Print      : expression",
        "Stmt Return     : keyword, value",
        "Stmt Var        : name, initializer",
        "Stmt While      : condition, body",
    ])


if __name__ == '__main__':
    main()
