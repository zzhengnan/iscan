import subprocess
import sys
from os import environ
from os.path import walk

from ..grandparentutils import baz
from ..parentutils import bar
from .utils import foo


def fuzz():
    try:
        import logging
    except ImportError:
        raise


def buzz():
    """import pandas as pd"""
    # import numpy as np
    print("import time")
