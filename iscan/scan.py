"""Utilities to scan all Python files in a directory and
aggregate the names of all the imported packages
"""
import argparse
import ast
import os
from collections import Counter
from typing import Dict, List, Optional, Tuple

from iscan.std_lib import separate_third_party_from_std_lib


class ImportScanner(ast.NodeVisitor):
    """Scanner to look for imported packages."""
    def __init__(self) -> None:
        self.imports = []  # type: ignore

    def visit_Import(self, node: ast.Import) -> None:
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

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
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

    def get_imports(self) -> List[str]:
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


def scan_directory(dir_to_scan: str, dir_to_exclude: Optional[str] = None) -> List[str]:
    """Extract packages imported across all Python files in a directory.

    Args:
        dir_to_scan: Path to the directory of interest
        dir_to_exclude: Path to the directory to be excluded during scanning

    Returns:
        Imported packages; might contain duplicates
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


def sort_counter(counter: Counter, alphabetical: bool) -> Dict[str, int]:
    """Sort counter according to custom logic.

    Args:
        counter: Imported packages and their corresponding count
        alphabetical: Whether to sort counter alphabetically

    Returns:
        Sorted counter
    """
    def custom_order(tup):
        # Sort first by count (descending), and then by name
        return -tup[1], tup[0]

    sort_key = None if alphabetical else custom_order
    return dict(sorted(counter.items(), key=sort_key))


def show_result(third_party: Dict[str, int], std_lib: Dict[str, int], ignore_std_lib: bool) -> None:
    """Print the result of running iscan.

    Args:
        third_party: Imported third-party packages and count
        std_lib: Imported standard library modules and count
        ignore_std_lib: Whether to omit standard library modules in the output
    """
    result = '''
--------------------------
   Third-party packages
--------------------------
NAME                 COUNT
'''
    for name, count in third_party.items():
        result += f'{name:<20} {count:>5}\n'

    if not ignore_std_lib:
        result += '''
--------------------------
 Standard library modules
--------------------------
NAME                 COUNT
'''
        for name, count in std_lib.items():
            result += f'{name:<20} {count:>5}\n'

    print(result)


def run(dir_to_scan: str, dir_to_exclude: Optional[str] = None) -> Tuple[Counter, Counter]:
    """Run iscan for a given set of parameters.

    Args:
        dir_to_scan: Path to the directory of interest
        dir_to_exclude: Path to the directory to be excluded during scanning

    Returns:
        Imported third-party packages and count
        Imported standard library modules and count
    """
    full_packages = scan_directory(dir_to_scan, dir_to_exclude)
    base_packages = map(get_base_name, full_packages)
    third_party, std_lib = separate_third_party_from_std_lib(base_packages)
    return Counter(third_party), Counter(std_lib)


def cli() -> argparse.Namespace:
    """Command line interface."""
    parser = argparse.ArgumentParser(
        allow_abbrev=False,
        description='Aggregate third-party packages and standard library modules imported across all Python files in a given directory.'  # noqa: E501
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
        help='whether to leave standard library modules out of the report'
    )
    parser.add_argument(
        '--alphabetical',
        dest='ALPHABETICAL',
        action='store_const',
        const=True,
        default=False,
        help='whether to sort the report alphabetically'
    )
    return parser.parse_args()


def main() -> None:
    args = cli()
    third_party, std_lib = run(args.DIR_TO_SCAN, args.DIR_TO_EXCLUDE)
    third_party = sort_counter(third_party, args.ALPHABETICAL)  # type: ignore
    std_lib = sort_counter(std_lib, args.ALPHABETICAL)  # type: ignore
    show_result(third_party, std_lib, args.IGNORE_STD_LIB)
