"""This module provides functionality to scan a directory and aggregate
the names of packages imported across all python files in said directory.
"""
import argparse
import ast
from os import walk
from os.path import abspath, join

from iscan.std_lib import filter_out_std_lib


class ImportScanner(ast.NodeVisitor):
    """Scanner to look for imported packages."""

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
        return sorted(self.imports)


def get_base_name(full_name: str) -> str:
    """Extract the base name of a package.

    Args:
        full_name: Full name of the package of interest, e.g., pandas.testing

    Returns:
        Base name of the provided package, e.g., pandas
    """
    return full_name.split('.')[0]


def convert_source_to_tree(fpath: str) -> ast.Module:
    """Convert source code into abstract syntax tree.

    Args:
        fpath: Path to the python file of interest

    Returns:
        AST representation of the source code
    """
    with open(fpath, 'r') as f:
        tree = ast.parse(f.read())
    return tree


def scan_directory(dir_to_scan: str, dir_to_exclude: str) -> list:
    """Extract names of unique packages imported across all python files in a directory.

    Args:
        dir_to_scan: Path to the directory of interest

    Returns:
        List of unique packages imported
    """
    all_imports = []
    for root_dir, _, fnames in walk(top=dir_to_scan):
        # Skip excluded directory
        if dir_to_exclude is not None:
            if abspath(dir_to_exclude) in abspath(root_dir):
                continue

        for fname in fnames:
            # Skip non-python files
            if not fname.endswith('.py'):
                continue

            # Convert source code into tree
            fpath = join(root_dir, fname)
            tree = convert_source_to_tree(fpath)

            # Extract imports for current file
            scanner = ImportScanner()
            scanner.visit(tree)
            all_imports.extend(scanner.get_imports())

    return sorted(set(map(get_base_name, all_imports)))


def cli() -> argparse.Namespace:
    """Command line interface."""
    parser = argparse.ArgumentParser(
        allow_abbrev=False,
        description='Scan python files in a given directory for third-party dependencies.'
    )
    parser.add_argument(
        'DIR_TO_SCAN',
        help='target directory to scan'
    )
    parser.add_argument(
        '-x',
        default=None,
        dest='DIR_TO_EXCLUDE',
        help='directory to exclude during scanning'
    )
    return parser.parse_args()


def main():
    args = cli()
    dir_to_scan, dir_to_exclude = args.DIR_TO_SCAN, args.DIR_TO_EXCLUDE

    unique_imports = scan_directory(dir_to_scan, dir_to_exclude)
    unique_imports = filter_out_std_lib(unique_imports)
    end = ', EXCLUDING those in {}\n'.format(dir_to_exclude) if dir_to_exclude else '\n'
    print(
        'Third-party packages imported across all python files in {}'.format(dir_to_scan),
        end=end
    )
    print(unique_imports)


if __name__ == '__main__':
    main()
