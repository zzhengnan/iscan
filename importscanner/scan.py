import os
import re
import sys


def remove_strings_and_comments(file_content):
    triple_quotes = '["\']{3}'
    triple_quotes = triple_quotes + '.*?' + triple_quotes
    triple_quotes = re.compile(triple_quotes, re.DOTALL)  # DOTALL allows matching of multi-line strings

    single_quote = '["\']'
    single_quote = single_quote + '.*?' + single_quote

    comment = '#+.*'

    for pattern_to_remove in [triple_quotes, single_quote, comment]:
        file_content = re.sub(pattern_to_remove, '', file_content)

    return file_content


def extract_package_name(line):
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


def collect_file_paths(path_to_repo):
    fpaths = []
    for root_dir, _, fnames in os.walk(top=path_to_repo):
        for fname in fnames:
            if fname.endswith('.py'):
                full_path = os.path.join(root_dir, fname)
                fpaths.append(full_path)
    return fpaths


def scan_file(file_content):
    imported_pkgs = []
    file_content = remove_strings_and_comments(file_content)
    lines = file_content.split('\n')
    for line in lines:
        pkg_name = extract_package_name(line)
        if pkg_name:
            imported_pkgs.append(pkg_name)
    return sorted(set(imported_pkgs))


def scan_repo(path_to_repo):
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
