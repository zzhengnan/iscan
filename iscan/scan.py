"""Utilities to scan all Python files in a directory and
aggregate the names of all the imported packages
"""
import argparse
import ast
import os

from iscan.std_lib import separate_third_party_from_std_lib


class ImportScanner(ast.NodeVisitor):
    """Scanner to look for imported packages."""
    def __init__(self):
        self.imports = []

    def visit_Import(self, node):
        """Extract imports of the form `import foo`.

        >>> import_statement = 'import os.path.join as jn, datetime.datetime as dt'
        >>> ast.dump(ast.parse(import_statement))
        "Module(body=[
            Import(names=[alias(name='os.path.join', asname='jn'),
                          alias(name='datetime.datetime', asname='dt')])
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
            ImportFrom(module='os.path',
                       names=[alias(name='join', asname='jn'),
                              alias(name='split', asname=None)],
                       level=0)
        ])"
        """
        # Ignore relative imports, for which node.level > 0
        # E.g., `from ..utils import foo` has a node.level of 2
        if node.level == 0:
            self.imports.append(node.module)
        self.generic_visit(node)

    def get_imports(self):
        return sorted(self.imports)


def convert_source_to_tree(fpath: str) -> ast.Module:
    """Convert source code into abstract syntax tree.

    Args:
        fpath: Path to the Python file of interest

    Returns:
        AST representation of the source code
    """
    with open(fpath, 'r') as f:
        tree = ast.parse(f.read())
    return tree


def scan_directory(dir_to_scan: str, dir_to_exclude: str) -> list:
    """Extract packages imported across all Python files in a directory.

    Args:
        dir_to_scan: Path to the directory of interest

    Returns:
        List of packages imported; might contain duplicates
    """
    all_imports = []
    for root_dir, _, fnames in os.walk(top=dir_to_scan):
        # Skip excluded directory
        if dir_to_exclude is not None:
            if os.path.abspath(dir_to_exclude) in os.path.abspath(root_dir):
                continue

        for fname in fnames:
            # Skip non-Python files
            if not fname.endswith('.py'):
                continue

            # Convert source code into tree
            fpath = os.path.join(root_dir, fname)
            tree = convert_source_to_tree(fpath)

            # Extract imports for current file
            scanner = ImportScanner()
            scanner.visit(tree)
            all_imports.extend(scanner.get_imports())

    return all_imports


def get_base_name(full_name: str) -> str:
    """Extract the base name of a package.

    Args:
        full_name: Full name of the package of interest, e.g., pandas.testing

    Returns:
        Base name of the provided package, e.g., pandas
    """
    return full_name.split('.')[0]


def get_unique_base_packages(packages: list) -> list:
    """Remove duplicates and extract the base package names.

    Args:
        packages: List of package names that might contain duplicates

    Returns:
        List of unique base package names
    """
    return sorted(set(map(get_base_name, packages)))


def show_result(third_party: list, std_lib: list, ignore_std_lib: bool) -> None:
    """Print the result of running iscan.

    Args:
        third_party: List of third-party packages
        std_lib: List of standard library modules
        ignore_std_lib: Whether to omit standard library modules in the output
    """
    print('\nThird-party packages:\n  - ', end='')
    print('\n  - '.join(third_party))

    if std_lib and not ignore_std_lib:
        print('\nStandard library modules:\n  - ', end='')
        print('\n  - '.join(std_lib))


def cli() -> argparse.Namespace:
    """Command line interface."""
    parser = argparse.ArgumentParser(
        allow_abbrev=False,
        description='Look for packages imported across all Python files in a given directory.'
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
    parser.add_argument(
        '--ignore-std-lib',
        dest='IGNORE_STD_LIB',
        action='store_const',
        const=True,
        default=False,
        help='whether to omit standard library modules'
    )
    return parser.parse_args()


def main():
    args = cli()

    all_imports = scan_directory(args.DIR_TO_SCAN, args.DIR_TO_EXCLUDE)
    unique_imports = get_unique_base_packages(all_imports)
    third_party, std_lib = separate_third_party_from_std_lib(unique_imports)

    print(
        f'Packages imported across all Python files in directory "{args.DIR_TO_SCAN}"',
        end=f', excluding "{args.DIR_TO_EXCLUDE}"\n' if args.DIR_TO_EXCLUDE else '\n'
    )

    show_result(third_party, std_lib, args.IGNORE_STD_LIB)
