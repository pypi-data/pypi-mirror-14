import ast
from collections import namedtuple

Import = namedtuple('Import', 'path name node')


def parse_file(filename):  # type: (str) -> ast.AST
    with open(filename, 'r') as fp:
        return ast.parse(fp.read(), filename=filename)


def get_import_list(node):  # type: (Union[ast.Import, ast.ImportFrom]) -> Generator[Import]
    assert isinstance(node, (ast.Import, ast.ImportFrom))

    if isinstance(node, ast.Import):
        # Example: import module as name
        for alias in node.names:
            assert isinstance(alias, ast.alias)

            path = alias.name
            name = alias.asname
            if name is None:
                name = path
            assert name is not None

            yield Import(path=path, name=name, node=alias)
    else:
        # Example: from module import submodule as name
        for alias in node.names:
            assert isinstance(alias, ast.alias)

            path = alias.name
            if node.module is not None:
                path = '{module}.{path}'.format(module=node.module, path=path)

            if node.level > 0:  # Example: from .foo import bar
                prefix = '.' * node.level
                path = prefix + path
            else:
                assert node.level == 0
                assert node.module is not None, "unnamed modules are only relative imports"

            name = alias.name
            if alias.asname is not None:
                name = alias.asname

            yield Import(path=path, name=name, node=alias)


def get_imports(tree):  # type: (ast.AST) -> Generator[Import]
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Import, ast.ImportFrom)):
            continue

        # BBB: This should be yield from, but this has to be compatible
        #      Python 2.7
        for elem in get_import_list(node):
            yield elem
