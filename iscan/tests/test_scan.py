from os.path import abspath, dirname, join

import pytest

from iscan.scan import (ImportScanner, convert_source_to_tree, get_base_name,
                        get_unique_base_packages, run, scan_directory)


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
    (None, ['ctypes', 'datetime', 'matplotlib.pyplot', 'numpy', 'os.path', 'pandas', 'shutil', 'time']),
    (join(CURRENT_DIR, 'test_package', 'city'), ['matplotlib.pyplot', 'numpy', 'os.path', 'pandas', 'shutil', 'time'])
])
def test_scan_directory(dir_to_exclude, expected):
    dir_to_scan = join(CURRENT_DIR, 'test_package')
    assert sorted(scan_directory(dir_to_scan, dir_to_exclude)) == expected


@pytest.mark.parametrize('full_name, expected', [
    ('foo', 'foo'),
    ('foo.bar', 'foo'),
    ('foo.bar.baz', 'foo'),
    ('foo_bar_baz.batman', 'foo_bar_baz')
])
def test_get_base_name(full_name, expected):
    assert get_base_name(full_name) == expected


@pytest.mark.parametrize('packages, expected', [
    (['foo', 'foo.bar'], ['foo']),
    (['foo.bar', 'bar.foo'], ['bar', 'foo']),
    (['foo', 'bar'], ['bar', 'foo']),
    (['foo_bar_baz.batman'], ['foo_bar_baz'])
])
def test_get_unique_base_packages(packages, expected):
    assert get_unique_base_packages(packages) == expected


@pytest.mark.parametrize('dir_to_exclude, expected', [
    (None, {
        'third_party': ['matplotlib', 'numpy', 'pandas'],
        'std_lib': ['ctypes', 'datetime', 'os', 'shutil', 'time']
    }),
    (join(CURRENT_DIR, 'test_package', 'city'), {
        'third_party': ['matplotlib', 'numpy', 'pandas'],
        'std_lib': ['os', 'shutil', 'time']
    })
])
def test_run(dir_to_exclude, expected):
    dir_to_scan = join(CURRENT_DIR, 'test_package')
    assert run(dir_to_scan, dir_to_exclude) == expected
