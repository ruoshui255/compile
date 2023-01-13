import sys

def define_AST(output_folder, filename, types: list[str]):
    """
    types: ["ExprBinary: left, operator, right"]
    """
    file = output_folder + "/" + filename
    with open(file, "w+", encoding="utf-8") as f:
        for type in types:
            class_name = type.split(":")[0].strip()
            file = output_folder + "/" + filename
            args = type.split(":")[1].strip()
            define_type(f, class_name, args)
            f.write("\n\n")


def define_type(f, class_name, fields):
    f.write("class " + class_name + ":\n")
    f.write("    def __init__(self, {}):\n".format(fields))

    for field in fields.split(", "):
        f.write("        self.{0} = {0}\n".format(field))

    f.write("\n")
    f.write("    def accept(self, visitor):\n")
    f.write("        return visitor.visit_{}(self)\n".format(class_name))


def main():
    if len(sys.argv) < 1:
        print("Usage: input <output folder>")
        exit(-1)

    output_folder = sys.argv[1]
    define_AST(output_folder, "../src/expr.py", [
        "ExprBinary   : left, operator, right",
        "ExprGrouping : expression",
        "ExprLiteral  : value",
        "ExprUnary    : operator, right"
    ])


if __name__ == '__main__':
    main()
