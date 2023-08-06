import ast
import astor
import argparse
import os
import sys
import colorama
import sphinx.quickstart


__version__ = 1.0


class RewriteShorthandLambda(ast.NodeTransformer):
    """An `ast.NodeTransformer` class which converts AmpliPy's alternative
    lambda syntax, which uses sets, into Python's lambda syntax.

    Examples:
        `{x | x + 1}` becomes `lambda x: x + 1`
        `{_ | print(42)}` becomes `lambda: print(42)`
        `{(x, y) | x + y}` becomes `lambda x, y: x + y`

    """
    def visit_Set(self, node):
        # Abort if the set isn't a single-element set
        if len(node.elts) != 1:
            return
        self.stmt = node.elts[0]

        # Abort if the set's only element isn't the Bitwise Or syntax
        if not isinstance(self.stmt, ast.BinOp):
            if isinstance(self.stmt, ast.Compare):
                print("{}WARNING: {}On line {}, a one-item set is being parsed"
                      " as `{}`. If this needs to be a lambda, please wrap"
                      " the body in brackets, like this: `{{x | (x == 0)}}`."
                      .format(colorama.Fore.YELLOW, colorama.Fore.WHITE,
                              node.lineno, astor.to_source(node)))
            return
        if not isinstance(self.stmt.op, ast.BitOr):
            return

        # Configure arguments for the resulting lambda
        self.args = ast.arguments(defaults=[], vararg=None, kwarg=None)
        if isinstance(self.stmt.left, ast.Tuple):
            if not all([isinstance(x, ast.Name) for x in self.stmt.left.elts]):
                raise SyntaxError("tuple before pipe in short lambda should "
                                  "contain only simple values")
            self.args.args = self.stmt.left.elts
        elif isinstance(self.stmt.left, ast.Name):
            self.args.args = [self.stmt.left]
        else:
            raise SyntaxError("value before pipe in short lambda should be "
                              "tuple of simple values or a simple value")

        # Replace the set with the lambda
        self.new_node = ast.Lambda(self.args, ast.Expr(node.elts[0].right))
        return ast.copy_location(self.new_node, node)


def main():
    colorama.init()

    # Set up the argument parser
    parser = argparse.ArgumentParser(
        description="Convert AmpliPy extended Python syntax into standard "
                    "Python code.")
    parser.add_argument("file", type=argparse.FileType("r"),
                        help="the AmpliPy file (.apy) to convert into Python.")
    parser.add_argument("-V", "--version", action="version",
                        version="AmpliPy {}".format(__version__))
    args = parser.parse_args()

    # Read the file and parse it
    syntax = ast.parse(args.file.read())
    RewriteShorthandLambda().visit(syntax)

    # Write to the new file
    new_path = os.path.splitext(args.file.name)[0] + ".py"
    if os.path.isfile(new_path):
        user_input = input("{}Output path \"{}\" already exists. Overwrite? {}"
                           .format(colorama.Fore.GREEN, new_path,
                                   colorama.Fore.WHITE))
        if not user_input.lower() in ["y", "yes"]:
            sys.exit(0)

    with open(new_path, "w") as f:
        print("Writing to {}...".format(new_path))
        f.write(astor.to_source(syntax))
        print("Complete.")


if __name__ == '__main__':
    main()
