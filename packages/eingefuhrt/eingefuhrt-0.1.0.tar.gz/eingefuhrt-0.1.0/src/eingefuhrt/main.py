import ast
import sys

from eingefuhrt.formatters import hacking
from eingefuhrt.parser import get_imports


def run():
    tree = ast.parse(sys.stdin.read(), '<stdin>')
    sys.stdout.write(hacking(get_imports(tree)))


if __name__ == '__main__':
    run()
