# `iscan`: Scan your project for its dependencies
Ever lost count of (or wondered) which packages your project depends on? `iscan` will give you a list of your project's direct dependencies.

## Installation
```
$ pip install iscan
```

## Usage
Specify the path to the directory you wish to scan; both absolute and relative paths are accepted.
```
$ iscan path/to/dir
```

Optionally, you can provide a second argument, specifying a directory to be _excluded_ when `iscan` looks for imported packages. For instance, the following command will scan all python files in the `foo` directory except those in `foo/tests`, which will be ignored.
```
$ iscan foo foo/tests
```

## Example output with `pandas`
Running the utility on a local clone of the [`pandas` repo](https://github.com/pandas-dev/pandas) produces the following. These are all the packages `pandas` imports directly.
```
$ iscan ~/Desktop/pandas/
Packages imported across all python files in pandas/
['AppKit', 'Foundation', 'IPython', 'PyQt4', 'PyQt5', '__main__', '_csv', 'abc', 'array', 'ast', 'botocore', 'bs4', 'builtins', 'bz2', 'calendar', 'cftime', 'codecs', 'collections', 'contextlib', 'copy', 'csv', 'ctypes', 'cycler', 'dask', 'dataclasses', 'datetime', 'dateutil', 'decimal', 'distutils', 'email', 'errno', 'fastparquet', 'fractions', 'functools', 'gc', 'glob', 'gzip', 'hashlib', 'http', 'hypothesis', 'importlib', 'inspect', 'io', 'itertools', 'jedi', 'json', 'keyword', 'locale', 'logging', 'lxml', 'lzma', 'math', 'matplotlib', 'mmap', 'mpl_toolkits', 'multiprocessing', 'numba', 'numbers', 'numexpr', 'numpy', 'odf', 'openpyxl', 'operator', 'optparse', 'os', 'pandas', 'pathlib', 'pg8000', 'pickle', 'pkg_resources', 'platform', 'pprint', 'psycopg2', 'py', 'pyarrow', 'pydoc', 'pylab', 'pymysql', 'pytest', 'pytz', 'pyxlsb', 'qtpy', 'random', 're', 's3fs', 'scipy', 'shutil', 'sklearn', 'sqlalchemy', 'sqlite3', 'statsmodels', 'string', 'struct', 'subprocess', 'sys', 'tables', 'tarfile', 'tempfile', 'textwrap', 'threading', 'time', 'token', 'tokenize', 'types', 'typing', 'unicodedata', 'urllib', 'uuid', 'warnings', 'weakref', 'xarray', 'xlrd', 'xlsxwriter', 'xlwt', 'zipfile']
```

If you are not interested in, say, packages imported during testing, you can specify the path to the tests directory for the entire directory to be ignored.
```
$ iscan ~/Desktop/pandas/ ~/Desktop/pandas/tests/
Packages imported across all python files in pandas/, EXCLUDING those in pandas/tests/
['AppKit', 'Foundation', 'IPython', 'PyQt4', 'PyQt5', '__main__', '_csv', 'abc', 'array', 'ast', 'botocore', 'bs4', 'builtins', 'bz2', 'calendar', 'codecs', 'collections', 'contextlib', 'copy', 'csv', 'ctypes', 'cycler', 'dataclasses', 'datetime', 'dateutil', 'decimal', 'distutils', 'email', 'errno', 'fastparquet', 'fractions', 'functools', 'gc', 'glob', 'gzip', 'hashlib', 'http', 'hypothesis', 'importlib', 'inspect', 'io', 'itertools', 'jedi', 'json', 'keyword', 'locale', 'logging', 'lxml', 'lzma', 'math', 'matplotlib', 'mmap', 'mpl_toolkits', 'multiprocessing', 'numba', 'numbers', 'numexpr', 'numpy', 'odf', 'openpyxl', 'operator', 'optparse', 'os', 'pandas', 'pathlib', 'pg8000', 'pickle', 'pkg_resources', 'platform', 'pprint', 'psycopg2', 'py', 'pyarrow', 'pydoc', 'pylab', 'pymysql', 'pytest', 'pytz', 'pyxlsb', 'qtpy', 'random', 're', 's3fs', 'scipy', 'shutil', 'sqlalchemy', 'sqlite3', 'string', 'struct', 'subprocess', 'sys', 'tables', 'tarfile', 'tempfile', 'textwrap', 'threading', 'time', 'token', 'tokenize', 'types', 'typing', 'unicodedata', 'urllib', 'uuid', 'warnings', 'weakref', 'xarray', 'xlrd', 'xlsxwriter', 'xlwt', 'zipfile']
```
