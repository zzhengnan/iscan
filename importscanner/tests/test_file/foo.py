"""This is just a lowly test module.
Nothing to see here.
"""


import subprocess
import sys
from os import environ
from os.path import walk


def foo():
    """Single-line docstring for better coverage."""
    try:
        import logging
    except:
        raise  # Random comment


### Random comment hanging out here ###
def bar():
    '''Multi-line docstring declared using single quotes
    should work too.'''
    print('This should be removed')


def baz():
    '''import pandas as pd'''
    # import numpy as np
    print("Hello!", 'world')
