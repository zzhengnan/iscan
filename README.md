# `iscan`: What are your dependencies?

[![python-versions](https://img.shields.io/pypi/pyversions/iscan)](https://github.com/zzhengnan/iscan)
[![license](https://img.shields.io/pypi/l/iscan)](https://github.com/zzhengnan/iscan/blob/main/LICENSE)
[![pypi](https://img.shields.io/pypi/v/iscan)](https://pypi.org/project/iscan/)
[![conda](https://img.shields.io/conda/vn/conda-forge/iscan)](https://anaconda.org/conda-forge/iscan)
[![downloads](https://pepy.tech/badge/iscan)](https://pepy.tech/project/iscan)
[![build_status](https://img.shields.io/github/workflow/status/zzhengnan/iscan/run-tests/main)](https://github.com/zzhengnan/iscan/actions/workflows/run-tests.yml)

Ever wondered which dependencies your Python project relies on?

`iscan` gives you a clear view of all the third-party packages and standard library modules imported by your project

- [1. Quick start](#1.-Quick-start)
- [2. Installation](#2.-Installation)
- [3. Dependencies](#3.-Dependencies)
- [4. Usage](#4.-Usage)
    - [4.1 Command line interface](#4.1-Command-line-interface)
    - [4.2 Python API](#4.2-Python-API)

## 1. Quick start
Simply provide the path to your project. That's it!

Here's an example of running `iscan` on a local clone of the popular HTTP library [requests](https://github.com/psf/requests/tree/v2.25.1). These are all the third-party packages and standard library modules `requests` relies on.
```
$ iscan ./requests/  # Executed at the top level of the requests repo
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

## 2. Installation
`iscan` can be installed with either conda or pip.
```
$ conda install iscan -c conda-forge
$ python -m pip install iscan
```

## 3. Dependencies
`iscan` is light-weight and doesn't rely on anything outside the standard library. The core functionality relies on the [ast](https://docs.python.org/3/library/ast.html#module-ast) module.

## 4. Usage
`iscan` provides both a command line interface and a Python API.

### 4.1 Command line interface
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

The complete help message can be accessed as follows.
```
$ iscan --help
```

### 4.2 Python API
The Python API exposes a `run` function that returns the scanning result as a dictionary, split between third-party packages and standard library modules.
```python
>>> from iscan import run
>>> dir_to_scan = './requests'
>>> dir_to_exclude = './tests'  # Use None to not exclude anything (default)
>>> result = run(dir_to_scan, dir_to_exclude)
>>> result
{'third_party': ['OpenSSL', 'certifi', 'chardet', 'cryptography', 'idna', 'simplejson', 'urllib3'],
 'std_lib': ['Cookie', 'StringIO', '__future__', '_winreg', 'base64', 'calendar', 'codecs', ...]}
```
