"""Modules in the standard library, scraped from https://docs.python.org/3/py-modindex.html
with the following code.

```
import requests
from bs4 import BeautifulSoup

def extract_std_lib(url):
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    std_lib = [link.text for link in soup.find('table').find_all('a', href=True)]
    std_lib = [module.split('.')[0] for module in std_lib]
    return sorted(set(std_lib))

url = 'https://docs.python.org/{version}/py-modindex.html'
cumulative = []
for version in ['2.7', '3.5', '3.6', '3.7', '3.8']:
    std_lib = extract_std_lib(url.format(version=version))
    print('\nNew additions in {}'.format(version))
    print([module for module in std_lib if module not in cumulative])
    cumulative.extend(std_lib)
```
"""
# Modules that come with the standard library in python 2.7
STD_LIB_27 = [
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
]

# New modules introduced in python 3.5+
STD_LIB_35 = [
    '_dummy_thread', '_thread',
    'asyncio', 'builtins', 'concurrent', 'configparser', 'copyreg', 'enum', 'faulthandler',
    'html', 'http', 'ipaddress', 'lzma',
    'pathlib', 'queue', 'reprlib', 'selectors', 'socketserver', 'statistics', 'tkinter', 'tracemalloc', 'turtledemo', 'typing',
    'venv', 'winreg', 'xmlrpc', 'zipapp'
]
STD_LIB_36 = ['secrets']
STD_LIB_37 = ['contextvars', 'dataclasses']
STD_LIB_38 = []

STD_LIB = STD_LIB_27 + STD_LIB_35 + STD_LIB_36 + STD_LIB_37 + STD_LIB_38


def filter_out_std_lib(orig_list: list) -> list:
    """Remove modules in the standard library from the given list.

    Args:
        orig_list: List of package names

    Returns:
        List of packages with modules in the standard library removed
    """
    return [i for i in orig_list if i not in STD_LIB]
