from os.path import abspath, dirname, join

import pytest

from iscan.scan import ImportScanner, convert_source_to_tree, get_base_name, scan_directory  # isort:skip # noqa: E501


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
    # This function doesn't do anything other than converting source code into its
    # AST representation using the ast module. No need to test
    assert True


@pytest.mark.parametrize('dir_to_exclude, expected', [
    (None, ['ctypes', 'datetime', 'matplotlib', 'numpy', 'os', 'pandas', 'shutil', 'time']),
    (join(CURRENT_DIR, 'test_package', 'city'), ['matplotlib', 'numpy', 'os', 'pandas', 'shutil', 'time'])  # noqa: E501
])
def test_scan_directory(dir_to_exclude, expected):
    dir_to_scan = join(CURRENT_DIR, 'test_package')
    assert scan_directory(dir_to_scan, dir_to_exclude) == expected
