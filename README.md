# `iscan`: Scan your project for third-party dependencies
Ever wondered which third-party dependencies your project relies on? `iscan` will give you a list of packages that are imported in your project which are _not_ part of the [standard library](https://docs.python.org/3/library/index.html).

## Installation
```
$ pip install iscan
```

## Dependencies
`iscan` is light-weight and doesn't rely on anything outside the standard library. The core functionality leverages the built-in [ast](https://docs.python.org/3/library/ast.html) module. `pytest` is an optional dependency for running tests.

## Usage
Specify the path to the directory you wish to scan. Both absolute and relative paths are accepted.
```
$ iscan path/to/dir
```

Optionally, you can provide a second argument to specify a directory to be _excluded_ when `iscan` looks for imported packages. For instance, the following command will scan all python files in the `foo` directory except those in `foo/tests`, which will be ignored.
```
$ iscan foo -x foo/tests
```

The complete help message is shown below.
```
$ iscan --help
usage: iscan [-h] [-x DIR_TO_EXCLUDE] DIR_TO_SCAN

Scan python files in a given directory for third-party
dependencies.

positional arguments:
  DIR_TO_SCAN        target directory to scan

optional arguments:
  -h, --help         show this help message and exit
  -x DIR_TO_EXCLUDE  directory to exclude during scanning
```

## Example output with `pandas`
Running the utility on a local clone of [pandas](https://github.com/pandas-dev/pandas) produces the following. These are all the packages `pandas` imports that are not part of the standard library.
```
$ iscan ~/Desktop/pandas/pandas/
Third-party packages imported across all python files in /Users/zhengnan/Desktop/pandas/pandas/
['AppKit', 'Foundation', 'IPython', 'PyQt4', 'PyQt5', '_csv', 'botocore', 'bs4', 'cftime', 'cycler', 'dask', 'dateutil', 'fastparquet', 'hypothesis', 'jedi', 'lxml', 'matplotlib', 'mpl_toolkits', 'numba', 'numexpr', 'numpy', 'odf', 'openpyxl', 'pandas', 'pg8000', 'pkg_resources', 'psycopg2', 'py', 'pyarrow', 'pylab', 'pymysql', 'pytest', 'pytz', 'pyxlsb', 'qtpy', 's3fs', 'scipy', 'sklearn', 'sqlalchemy', 'statsmodels', 'tables', 'xarray', 'xlrd', 'xlsxwriter', 'xlwt']
```

If you are not interested in, say, packages imported during testing, you can specify the path to the tests directory for the entire directory to be ignored.
```
$ iscan ~/Desktop/pandas/pandas/ -x ~/Desktop/pandas/pandas/tests/
Third-party packages imported across all python files in /Users/zhengnan/Desktop/pandas/pandas/, EXCLUDING those in /Users/zhengnan/Desktop/pandas/pandas/tests/
['AppKit', 'Foundation', 'IPython', 'PyQt4', 'PyQt5', '_csv', 'botocore', 'bs4', 'cycler', 'dateutil', 'fastparquet', 'hypothesis', 'jedi', 'lxml', 'matplotlib', 'mpl_toolkits', 'numba', 'numexpr', 'numpy', 'odf', 'openpyxl', 'pandas', 'pg8000', 'pkg_resources', 'psycopg2', 'py', 'pyarrow', 'pylab', 'pymysql', 'pytest', 'pytz', 'pyxlsb', 'qtpy', 's3fs', 'scipy', 'sqlalchemy', 'tables', 'xarray', 'xlrd', 'xlsxwriter', 'xlwt']
```
