"""Modules in the standard library."""
import itertools
from typing import Iterable, List, Tuple


# Standard library modules in Python 2.7 and new modules since 3.5+
STD_LIB_BY_VERSION = {
    '2.7': [
        '__builtin__', '__future__', '__main__', '_winreg',
        'abc', 'aepack', 'aetools', 'aetypes', 'aifc', 'al', 'AL', 'anydbm', 'applesingle', 'argparse', 'array', 'ast', 'asynchat', 'asyncore', 'atexit', 'audioop', 'autoGIL',
        'base64', 'BaseHTTPServer', 'Bastion', 'bdb', 'binascii', 'binhex', 'bisect', 'bsddb', 'buildtools', 'bz2',
        'calendar', 'Carbon', 'cd', 'cfmfile', 'cgi', 'CGIHTTPServer', 'cgitb', 'chunk', 'cmath', 'cmd', 'code', 'codecs', 'codeop', 'collections', 'ColorPicker', 'colorsys', 'commands', 'compileall', 'compiler', 'ConfigParser', 'contextlib', 'Cookie', 'cookielib', 'copy', 'copy_reg', 'cPickle', 'cProfile', 'crypt', 'cStringIO', 'csv', 'ctypes', 'curses',
        'datetime', 'dbhash', 'dbm', 'decimal', 'DEVICE', 'difflib', 'dircache', 'dis', 'distutils', 'dl', 'doctest', 'DocXMLRPCServer', 'dumbdbm', 'dummy_thread', 'dummy_threading',
        'EasyDialogs', 'email', 'encodings', 'ensurepip', 'errno', 'exceptions',
        'fcntl', 'filecmp', 'fileinput', 'findertools', 'fl', 'FL', 'flp', 'fm', 'fnmatch', 'formatter', 'fpectl', 'fpformat', 'fractions', 'FrameWork', 'ftplib', 'functools', 'future_builtins',
        'gc', 'gdbm', 'gensuitemodule', 'getopt', 'getpass', 'gettext', 'gl', 'GL', 'glob', 'grp', 'gzip',
        'hashlib', 'heapq', 'hmac', 'hotshot', 'htmlentitydefs', 'htmllib', 'HTMLParser', 'httplib',
        'ic', 'icopen', 'imageop', 'imaplib', 'imgfile', 'imghdr', 'imp', 'importlib', 'imputil', 'inspect', 'io', 'itertools',
        'jpeg', 'json',
        'keyword',
        'lib2to3', 'linecache', 'locale', 'logging',
        'macerrors', 'MacOS', 'macostools', 'macpath', 'macresource', 'mailbox', 'mailcap', 'marshal', 'math', 'md5', 'mhlib', 'mimetools', 'mimetypes', 'MimeWriter', 'mimify', 'MiniAEFrame', 'mmap', 'modulefinder', 'msilib', 'msvcrt', 'multifile', 'multiprocessing', 'mutex',
        'Nav', 'netrc', 'new', 'nis', 'nntplib', 'numbers',
        'operator', 'optparse', 'os', 'ossaudiodev',
        'parser', 'pdb', 'pickle', 'pickletools', 'pipes', 'PixMapWrapper', 'pkgutil', 'platform', 'plistlib', 'popen2', 'poplib', 'posix', 'posixfile', 'pprint', 'profile', 'pstats', 'pty', 'pwd', 'py_compile', 'pyclbr', 'pydoc',
        'Queue', 'quopri',
        'random', 're', 'readline', 'resource', 'rexec', 'rfc822', 'rlcompleter', 'robotparser', 'runpy',
        'sched', 'ScrolledText', 'select', 'sets', 'sgmllib', 'sha', 'shelve', 'shlex', 'shutil', 'signal', 'SimpleHTTPServer', 'SimpleXMLRPCServer', 'site', 'smtpd', 'smtplib', 'sndhdr', 'socket', 'SocketServer', 'spwd', 'sqlite3', 'ssl', 'stat', 'statvfs', 'string', 'StringIO', 'stringprep', 'struct', 'subprocess', 'sunau', 'sunaudiodev', 'SUNAUDIODEV', 'symbol', 'symtable', 'sys', 'sysconfig', 'syslog',
        'tabnanny', 'tarfile', 'telnetlib', 'tempfile', 'termios', 'test', 'textwrap', 'thread', 'threading', 'time', 'timeit', 'Tix', 'Tkinter', 'token', 'tokenize', 'trace', 'traceback', 'ttk', 'tty', 'turtle', 'types',
        'unicodedata', 'unittest', 'urllib', 'urllib2', 'urlparse', 'user', 'UserDict', 'UserList', 'UserString', 'uu', 'uuid',
        'videoreader',
        'W', 'warnings', 'wave', 'weakref', 'webbrowser', 'whichdb', 'winsound', 'wsgiref',
        'xdrlib', 'xml', 'xmlrpclib',
        'zipfile', 'zipimport', 'zlib'
    ],
    '3.5': [
        '_dummy_thread', '_thread',
        'asyncio', 'builtins', 'concurrent', 'configparser', 'copyreg', 'enum', 'faulthandler',
        'html', 'http', 'ipaddress', 'lzma',
        'pathlib', 'queue', 'reprlib', 'selectors', 'socketserver', 'statistics', 'tkinter', 'tracemalloc', 'turtledemo', 'typing',
        'venv', 'winreg', 'xmlrpc', 'zipapp'
    ],
    '3.6': ['secrets'],
    '3.7': ['contextvars', 'dataclasses'],
    '3.8': [],
    '3.9': ['graphlib', 'zoneinfo'],
    '3.10': ['idlelib'],
    '3.11': ['_tkinter', 'sitecustomize', 'tomllib', 'usercustomize'],
    '3.12': [],
    '3.13': [],
}
STD_LIB = list(itertools.chain.from_iterable(STD_LIB_BY_VERSION.values()))  # type: ignore


def separate_third_party_from_std_lib(packages: Iterable[str]) -> Tuple[List[str], List[str]]:
    """Separate third-party packages from standard library modules.

    Args:
        packages: Package names

    Returns:
        Third-party packages, standard library modules
    """
    third_party, std_lib = [], []
    for package in packages:
        if package in STD_LIB:
            std_lib.append(package)
        else:
            third_party.append(package)
    return third_party, std_lib


def get_std_lib(version: str) -> List[str]:
    """Scrape modules in the standard library for a given Python version.

    Args:
        version: Python version

    Returns:
        Standard library modules for a given Python version
    """
    import requests  # type: ignore
    from bs4 import BeautifulSoup  # type: ignore

    url = f'https://docs.python.org/{version}/py-modindex.html'
    resp = requests.get(url)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, 'html.parser')
    links = soup.find('table').find_all('a', href=True)
    std_lib = [link.text.split('.')[0] for link in links]

    return sorted(set(std_lib))


if __name__ == '__main__':
    cumulative = []
    for py_version in STD_LIB_BY_VERSION.keys():
        std_lib = get_std_lib(py_version)
        print(f'\nNew additions in {py_version}')
        print([module for module in std_lib if module not in cumulative])
        cumulative.extend(std_lib)
