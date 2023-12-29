# `iscan`: What are your dependencies?

[![python-versions](https://img.shields.io/pypi/pyversions/iscan)](https://github.com/zzhengnan/iscan)
[![license](https://img.shields.io/pypi/l/iscan)](https://github.com/zzhengnan/iscan/blob/main/LICENSE)
[![pypi](https://img.shields.io/pypi/v/iscan)](https://pypi.org/project/iscan/)
[![conda](https://img.shields.io/conda/vn/conda-forge/iscan)](https://anaconda.org/conda-forge/iscan)
[![downloads](https://pepy.tech/badge/iscan)](https://pepy.tech/project/iscan)

Ever wondered which dependencies your Python project relies on? `iscan` gives you a clear view of all the third-party packages and standard library modules your project uses.

- [Installation](#installation)
- [Quick start](#quick-start)
- [Dependencies](#dependencies)
- [Usage](#usage)
    - [Command line interface](#command-line-interface)
    - [Python API](#python-api)

## Installation
`iscan` can be installed using either conda or pip.
```
$ conda install iscan -c conda-forge
$ python -m pip install iscan
```

## Quick start
Simply provide the path to your project. That's it!

Here's an example of running `iscan` on a local clone of the popular HTTP library [requests](https://github.com/psf/requests/tree/v2.25.1); these are all the third-party packages and standard library modules `requests` relies on, along with their respective import counts.
```
$ iscan ./requests/  # Executed at the top level of the requests repo

--------------------------
   Third-party packages
--------------------------
NAME                 COUNT
urllib3                 27
chardet                  3
cryptography             2
idna                     2
OpenSSL                  1
certifi                  1
simplejson               1

--------------------------
 Standard library modules
--------------------------
NAME                 COUNT
collections              6
sys                      6
os                       4
io                       3
time                     3
urllib                   3
warnings                 3
...
```

## Dependencies
`iscan` is light-weight and doesn't rely on anything outside the standard library. The core scanning functionality is built on top of the [ast](https://docs.python.org/3/library/ast.html#module-ast) module.

## Usage
`iscan` provides both a command line interface and a Python API.

### Command line interface
Basic usage requires simply providing the path to the directory you wish to scan.

```
$ iscan path/to/dir
```

The following optional parameters are available
- `-x` allows a directory and its content to be _excluded_ during scanning
- `--ignore-std-lib` leaves standard library modules out of the report
- `--alphabetical` sorts the report alphabetically; the default is to sort on import count, in descending order

As a concrete example, the following invocation will report third-party packages imported across all Python files in the `requests/` directory, in alphabetical order; everything in `tests/` will be ignored, as will standard library modules.

```
$ iscan ./requests/ -x ./tests/ --ignore-std-lib --alphabetical

--------------------------
   Third-party packages
--------------------------
NAME                 COUNT
OpenSSL                  1
certifi                  1
chardet                  3
cryptography             2
idna                     2
simplejson               1
urllib3                 27
```

The complete help message can be accessed as follows.
```
$ iscan --help
```

### Python API
The Python API exposes a `run` function that returns the scanning result and import count in the form of two [Counter](https://docs.python.org/3/library/collections.html#collections.Counter) objects, split between third-party packages and standard library modules.
```python
>>> from iscan import run
>>> dir_to_scan = './requests'
>>> dir_to_exclude = './tests'  # Use None to not exclude anything (default)
>>> third_party, std_lib = run(dir_to_scan, dir_to_exclude)

>>> from pprint import pprint
>>> pprint(third_party)
Counter({'urllib3': 27,
         'chardet': 3,
         'idna': 2,
         'cryptography': 2,
         'simplejson': 1,
         'certifi': 1,
         'OpenSSL': 1})
>>> pprint(std_lib)
Counter({'collections': 6,
         'sys': 6,
         'os': 4,
         'time': 3,
         'warnings': 3,
         'io': 3,
         'urllib': 3,
         ...})
```
