import re
from pathlib import Path

import setuptools

from iscan import __version__ as VERSION


with open('README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()


setuptools.setup(
    name='iscan',
    version=VERSION,
    author='Zhengnan Zhao',
    description='iscan helps you identify your project\'s third-party dependencies',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/ZhengnanZhao/iscan',
    packages=setuptools.find_packages(),
    extras_require={
        'build': ['setuptools', 'twine', 'wheel'],
        'dev': ['pytest']
    },
    entry_points={'console_scripts': ['iscan=iscan.scan:main']},
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5'
)
