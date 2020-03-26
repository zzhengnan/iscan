"""This module provides functionality to scan a repo and
extract the names of packages imported in said repo.
"""


import ast
import os
import re
import sys


class ImportScanner(ast.NodeVisitor):
    """Scanner to look for import statements.

    Based on Matt Layman's work at
    https://www.mattlayman.com/blog/2018/decipher-python-ast/
    """
    def __init__(self):
        self.imports = []

    def visit_Import(self, node):
        imports = [alias.name for alias in node.names]
        self.imports.extend(imports)
        self.generic_visit(node)

    def visit_FromImport(self, node):
        imports = [alias.name for alias in node.names]
        self.imports.extend(imports)
        self.generic_visit(node)

    def report(self):
        return self.imports


def collect_file_paths(path_to_repo: str) -> list:
    """Collect all python files in a repo.

    Python files refer specifically to files with a .py extension.

    Args:
        path_to_repo: Path to the repo of interest.

    Returns:
        List of python files in the repo.
    """
    fpaths = []
    for root_dir, _, fnames in os.walk(top=path_to_repo):
        for fname in fnames:
            if fname.endswith('.py'):
                full_path = os.path.join(root_dir, fname)
                fpaths.append(full_path)
    return fpaths


def extract_unique_packages(packages: list) -> list:
    """Extract unique package names.

    Each element in the returned list is the base name of a package.
    E.g., if pandas.testing is provided as an input, pandas will get returned.

    Args:
        packages: A list of packages that may contain duplicates.

    Returns:
        List of unique package names.
    """
    unique_packages = []
    for package in packages:
        base_name = re.search(r'(\w+).*', package).groups()[0]
        unique_packages.append(base_name)
    return sorted(set(unique_packages))


def scan_repo(path_to_repo: str) -> list:
    """Extract names of unique packages imported in a repo.

    Args:
        path_to_repo: Path to the repo of interest.

    Returns:
        List of unique packages imported in the repo.
    """
    fpaths_to_scan = collect_file_paths(path_to_repo)
    scanner = ImportScanner()
    for fpath in fpaths_to_scan:
        with open(fpath, 'r') as f:
            file_ast = ast.parse(f.read())
        scanner.visit(file_ast)
    unique_packages = extract_unique_packages(scanner.report())
    return unique_packages


def main():
    path_to_repo = sys.argv[1]
    unique_packages = scan_repo(path_to_repo)
    print('\n'.join(unique_packages))


if __name__ == '__main__':
    main()
