"""This module provides functionality to scan a repo and aggregate
the names of packages imported across all python files.
"""


import ast
import os
import re
import sys


class ImportScanner(ast.NodeVisitor):
    """Scanner to look for import statements."""

    def __init__(self):
        self.imports = []

    def visit_Import(self, node):
        """Extract imports of the form `import foo`.

        >>> import_statement = 'import os.path.join as jn, datetime.datetime as dt'
        >>> ast.dump(ast.parse(import_statement))
        "Module(body=[
            Import(
                names=[alias(name='os.path.join', asname='jn'),
                       alias(name='datetime.datetime', asname='dt')]
            )
        ])"
        """
        for alias in node.names:
            self.imports.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """Extract imports of the form `from foo import bar`.

        Relative imports such as `from ..utils import foo` will be ignored.

        >>> import_statement = 'from os.path import join as jn, split'
        >>> ast.dump(ast.parse(import_statement))
        "Module(body=[
            ImportFrom(
                module='os.path',
                names=[alias(name='join', asname='jn'),
                       alias(name='split', asname=None)],
                level=0
            )
        ])"
        """
        # Ignore relative imports, for which node.level > 0
        # E.g., `from ..utils import foo` has a node.level of 2
        if node.level == 0:
            self.imports.append(node.module)
        self.generic_visit(node)

    def get_imports(self):
        return self.imports


def get_base_name(full_name: str) -> str:
    """Extract the base name of a package/module.

    Args:
        full_name: Full name of the package/module of interest. E.g., pandas.testing

    Returns:
        base_name: Base name of the provided package/module. E.g., pandas
    """
    pattern = r'(\w+).*'
    base_name = re.search(pattern, full_name).groups()[0]
    return base_name


def convert_source_to_tree(fpath: str) -> ast.Module:
    if fpath.endswith('.py'):
        with open(fpath, 'r') as f:
            tree = ast.parse(f.read())
        return tree


def scan_repo(path_to_repo: str) -> list:
    """Extract names of unique packages imported in a repo.

    Args:
        path_to_repo: Path to the repo of interest

    Returns:
        List of unique packages imported in the repo
    """
    all_imports = []
    for root_dir, subdirs, fnames in os.walk(top=path_to_repo):
        # TODO: Get name of package under investigation and add to this
        local_modules = subdirs + [fname.replace('.py', '') for fname in fnames]

        for fname in fnames:
            # Convert source code into tree
            fpath = os.path.join(root_dir, fname)
            tree = convert_source_to_tree(fpath)

            # Extract imports for current file
            scanner = ImportScanner()
            scanner.visit(tree)
            current_imports = map(get_base_name, scanner.get_imports())
            current_imports = [imp for imp in current_imports if imp not in local_modules]
            all_imports.extend(current_imports)

    return sorted(set(all_imports))


def main():
    path_to_repo = sys.argv[1]
    unique_imports = scan_repo(path_to_repo)
    print('\n'.join(unique_imports))


if __name__ == '__main__':
    main()
