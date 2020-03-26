import os

import importscanner.scan as scan


PATH_TO_CURRENT_DIR = os.path.join(os.path.dirname(__file__))


def test_collect_file_paths():
    path_to_repo = '{}/test_repo'.format(PATH_TO_CURRENT_DIR)
    expected = [
        '{}/test_repo/__init__.py'.format(PATH_TO_CURRENT_DIR),
        '{}/test_repo/foo/d.py'.format(PATH_TO_CURRENT_DIR),
        '{}/test_repo/foo/baz/c.py'.format(PATH_TO_CURRENT_DIR)
    ]
    assert scan.collect_file_paths(path_to_repo) == expected


def test_scan_repo():
    path_to_repo = '{}/test_repo'.format(PATH_TO_CURRENT_DIR)
    expected = ['pandas', 'time']
    assert scan.scan_repo(path_to_repo) == expected
