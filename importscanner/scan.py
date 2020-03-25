"""This module provides functionality to scan a repo and extract the names
of packages imported in said repo."""


import os
import re
import sys


def remove_strings_and_comments(file_content: str) -> str:
    """Remove strings and comments from a file.

    All forms of single- and multi-line strings enclosed in single (e.g., 'foo' and "foo")
    and triple quotes will be removed. Likewise, all forms of single-, multi-line,
    and inline comments will be removed.

    Args:
        file_content: Original string representation of a file.

    Returns:
        Content of the original file stripped of strings and comments.
    """
    for pattern_to_remove in ['"{3}.*?"{3}', "'{3}.*?'{3}"]:
        pattern_to_remove = re.compile(pattern_to_remove, re.DOTALL)  # DOTALL allows matching of multi-line strings
        file_content = re.sub(pattern_to_remove, '', file_content)

    for pattern_to_remove in ['".*?"', "'.*?'", '#+.*']:
        file_content = re.sub(pattern_to_remove, '', file_content)

    return file_content


def extract_package_name(line: str) -> str:
    """Extract name of the imported package from a line.

    Work with both forms of import statements.
    >>> import pandas as pd
    >>> from pandas import DataFrame

    Known issue: Does not work when importing multiple packages on the same line.
    >>> import pandas as pd, numpy as np

    Args:
        line: A single line from a source file.

    Returns:
        Name of the imported package if applicable, and None otherwise.
    """
    # Spaces and comments are ignored with the VERBOSE flag
    pattern_1 = re.compile(
        r"""^\s*        # 0 or more spaces. Need the ^ to distinguish from the second pattern
            import \s+  # The word "import" followed by 1 or more spaces
            (\w+)""",   # Name of the package
        re.VERBOSE
    )
    match_1 = re.search(pattern_1, line)
    if match_1:
        return match_1.groups()[0]

    pattern_2 = re.compile(
        r"""\s*        # 0 or more spaces
            from \s+   # The word "from" followed by 1 or more spaces
            (\w+)""",  # Name of the package
        re.VERBOSE
    )
    match_2 = re.search(pattern_2, line)
    if match_2:
        return match_2.groups()[0]

    return None


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


def scan_file(file_content: str) -> list:
    """Extract names of unique packages imported in a file.

    Args:
        file_content: String representation of a file.

    Returns:
        List of unique packages imported in the file.
    """
    imported_pkgs = []
    file_content = remove_strings_and_comments(file_content)
    lines = file_content.split('\n')
    for line in lines:
        pkg_name = extract_package_name(line)
        if pkg_name:
            imported_pkgs.append(pkg_name)
    return sorted(set(imported_pkgs))


def scan_repo(path_to_repo: str) -> list:
    """Extract names of unique packages imported in a repo.

    Args:
        path_to_repo: Path to the repo of interest.

    Returns:
        List of unique packages imported in the repo.
    """
    imported_pkgs = []
    fpaths_to_scan = collect_file_paths(path_to_repo)
    for fpath in fpaths_to_scan:
        with open(fpath, 'r') as f:
            file_content = f.read()
        imported_pkgs.extend(scan_file(file_content))
    return sorted(set(imported_pkgs))


def main():
    path_to_repo = sys.argv[1]
    imported_pkgs = scan_repo(path_to_repo)
    print('\n'.join(imported_pkgs))


if __name__ == '__main__':
    main()
