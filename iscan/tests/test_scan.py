from os.path import abspath, dirname, join

import pytest

from iscan.scan import ImportScanner, get_base_name, convert_source_to_tree, scan_directory


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


@pytest.mark.parametrize('full_name, expected', [
    ('foo', 'foo'),
    ('foo.bar', 'foo'),
    ('foo.bar.baz', 'foo'),
    ('foo_bar_baz.batman', 'foo_bar_baz')
])
def test_get_base_name(full_name, expected):
    assert get_base_name(full_name) == expected


def test_convert_source_to_tree():
    pass


def test_scan_directory():
    path_to_dir = join(CURRENT_DIR, 'test_package')
    expected = ['matplotlib', 'numpy', 'os', 'pandas', 'shutil', 'time']
    assert scan_directory(path_to_dir) == expected
