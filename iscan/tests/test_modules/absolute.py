import subprocess
import sys
from os import environ
from os.path import walk


def foo():
    try:
        import logging
    except ImportError:
        raise


def bar():
    """import pandas as pd"""
    # import numpy as np
    print("import time")
