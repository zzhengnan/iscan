from collections import Counter
from os.path import abspath, dirname, join

import pytest

from iscan.scan import (ImportScanner, convert_source_to_tree, get_base_name,
                        run, scan_directory, sort_counter)


CURRENT_DIR = abspath(dirname(__file__))


@pytest.mark.parametrize('module_name, expected', [
    ('absolute.py', ['logging', 'os', 'os.path', 'subprocess', 'sys']),
    ('relative.py', []),
    ('mixed.py', ['logging', 'os', 'os.path', 'subprocess', 'sys']),
])
def test_import_scanner(module_name, expected):
    path_to_module = join(CURRENT_DIR, 'test_modules', module_name)
    tree = convert_source_to_tree(path_to_module)
    scanner = ImportScanner()
    scanner.visit(tree)
    assert scanner.get_imports() == expected


@pytest.mark.parametrize('dir_to_exclude, expected', [
    (None, {'ctypes', 'datetime', 'matplotlib.pyplot', 'numpy', 'os.path', 'pandas', 'shutil', 'time'}),
    (join(CURRENT_DIR, 'test_package', 'city'), {'matplotlib.pyplot', 'numpy', 'os.path', 'pandas', 'shutil', 'time'})
])
def test_scan_directory(dir_to_exclude, expected):
    dir_to_scan = join(CURRENT_DIR, 'test_package')
    assert set(scan_directory(dir_to_scan, dir_to_exclude)) == expected


@pytest.mark.parametrize('full_name, expected', [
    ('foo', 'foo'),
    ('foo.bar', 'foo'),
    ('foo.bar.baz', 'foo'),
    ('foo_bar_baz.batman', 'foo_bar_baz')
])
def test_get_base_name(full_name, expected):
    assert get_base_name(full_name) == expected


@pytest.mark.parametrize('dir_to_exclude, expected', [
    (None, (
        {'matplotlib': 1, 'numpy': 2, 'pandas': 1},
        {'ctypes': 1, 'datetime': 1, 'os': 1, 'shutil': 2, 'time': 2}
    )),
    (join(CURRENT_DIR, 'test_package', 'city'), (
        {'matplotlib': 1, 'numpy': 2, 'pandas': 1},
        {'os': 1, 'shutil': 2, 'time': 2}
    ))
])
def test_run(dir_to_exclude, expected):
    dir_to_scan = join(CURRENT_DIR, 'test_package')
    assert run(dir_to_scan, dir_to_exclude) == expected


@pytest.mark.parametrize('alphabetical, expected', [
    (True, ['a', 'b', 'c', 'd']),
    (False, ['d', 'a', 'c', 'b'])
])
def test_sort_counter(alphabetical, expected):
    orig = Counter({'b': 1, 'a': 2, 'c': 2, 'd': 4})
    computed_keys = list(sort_counter(orig, alphabetical))
    assert computed_keys == expected
