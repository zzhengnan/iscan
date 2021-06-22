from time import time

import numpy


def baz_func():
    import shutil

    from .utils import nothing
    try:
        from os.path import join
    except ImportError:
        pass
