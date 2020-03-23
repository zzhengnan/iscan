import os

import importscanner.scan as scan


PATH_TO_CURRENT_DIR = os.path.join(os.path.dirname(__file__))


def test_remove_strings_and_comments():
    path_to_orig = '{}/test_file/foo.py'.format(PATH_TO_CURRENT_DIR)
    with open(path_to_orig, 'r') as f:
        orig = f.read()

    path_to_expected = '{}/test_file/foo_without_strings_or_comments.py'.format(PATH_TO_CURRENT_DIR)
    with open(path_to_expected, 'r') as f:
        expected = f.read()

    assert scan.remove_strings_and_comments(orig) == expected


def test_collect_file_paths():
    path_to_repo = '{}/test_repo'.format(PATH_TO_CURRENT_DIR)
    expected = [
        '{}/test_repo/__init__.py'.format(PATH_TO_CURRENT_DIR),
        '{}/test_repo/foo/d.py'.format(PATH_TO_CURRENT_DIR),
        '{}/test_repo/foo/baz/c.py'.format(PATH_TO_CURRENT_DIR)
    ]
    assert scan.collect_file_paths(path_to_repo) == expected


def test_scan_file():
    path_to_file = '{}/test_file/foo.py'.format(PATH_TO_CURRENT_DIR)
    with open(path_to_file, 'r') as f:
        file_content = f.read()

    expected = ['logging', 'os', 'subprocess', 'sys']
    assert scan.scan_file(file_content) == expected


def test_scan_repo():
    path_to_repo = '{}/test_repo'.format(PATH_TO_CURRENT_DIR)
    expected = ['pandas', 'time']
    assert scan.scan_repo(path_to_repo) == expected
