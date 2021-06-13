# `iscan`: What are your dependencies?

[![python-versions](https://img.shields.io/pypi/pyversions/iscan)](https://github.com/zzhengnan/iscan)
[![license](https://img.shields.io/pypi/l/iscan)](https://github.com/zzhengnan/iscan/blob/main/LICENSE)
[![pypi](https://img.shields.io/pypi/v/iscan)](https://pypi.org/project/iscan/)
[![conda](https://img.shields.io/conda/vn/conda-forge/iscan)](https://anaconda.org/conda-forge/iscan)
[![downloads](https://pepy.tech/badge/iscan)](https://pepy.tech/project/iscan)
[![build_status](https://img.shields.io/github/workflow/status/zzhengnan/iscan/run-tests/main)](https://github.com/zzhengnan/iscan/actions/workflows/run-tests.yml)

Ever wondered which dependencies your Python project relies on?

`iscan` gives you a clear view of all the third-party packages imported by your project, along with modules in the standard library.

- [Example](#Example)
- [Installation](#Installation)
- [Dependencies](#Dependencies)
- [Usage](#Usage)

## Example
Running `iscan` on a local clone of the popular HTTP library [requests](https://github.com/psf/requests/tree/v2.25.1) gives the following results -- these are all the third-party packages and standard library modules `requests` relies on.
```
$ iscan ./requests/  # From the top level of the requests repo
Packages imported across all Python files in directory "./requests/"

Third-party packages:
  - OpenSSL
  - certifi
  - chardet
  - cryptography
  - idna
  - simplejson
  - urllib3

Standard library modules:
  - Cookie
  - StringIO
  - __future__
  - _winreg
  - base64
  - calendar
  - codecs
  ...
```

## Installation
`iscan` can be installed with either conda or pip.
```
$ conda install iscan -c conda-forge
$ python -m pip install iscan
```

## Dependencies
`iscan` is light-weight and doesn't rely on anything outside the standard library. The core functionality relies on the [ast](https://docs.python.org/3/library/ast.html#module-ast) module.

## Usage
Basic usage requires simply providing the path to the directory you wish to scan.

```
$ iscan path/to/dir
```

The following optional parameters are available
- `-x` allows a directory to be _excluded_ from the scanning
- `--ignore-std-lib` suppresses scanning results for the standard library modules

As a concrete example, the following invocation will report third-party packages imported in the `requests/` directory; everything in `tests/` will be ignored, as will standard library modules.

```
$ iscan ./requests/ -x ./tests/ --ignore-std-lib
Packages imported across all Python files in directory "./requests/", excluding "./tests/"

Third-party packages:
  - OpenSSL
  - certifi
  - chardet
  - cryptography
  - idna
  - simplejson
  - urllib3
```

The complete help message is shown below.
```
$ iscan --help
usage: iscan [-h] [-x DIR_TO_EXCLUDE] [--ignore-std-lib] DIR_TO_SCAN

Look for packages imported across all Python files in a given directory.

positional arguments:
  DIR_TO_SCAN        target directory to scan

optional arguments:
  -h, --help         show this help message and exit
  -x DIR_TO_EXCLUDE  directory to exclude during scanning
  --ignore-std-lib   whether to omit standard library modules
```
