import setuptools

import iscan


with open('README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()


EXTRAS_REQUIRE = {
    'build': ['setuptools', 'twine', 'wheel'],
    'qa': ['flake8', 'mypy', 'pre-commit'],
    'test': ['pytest'],
    'util': ['beautifulsoup4', 'requests']  # To scrape modules from the standard library
}
EXTRAS_REQUIRE['dev'] = EXTRAS_REQUIRE['build'] + EXTRAS_REQUIRE['qa'] + EXTRAS_REQUIRE['test'] + EXTRAS_REQUIRE['util']  # noqa: E501


setuptools.setup(
    name='iscan',
    version=iscan.__version__,
    url='https://github.com/zzhengnan/iscan',
    author='Zhengnan Zhao',
    description='iscan helps you identify your project\'s third-party dependencies',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    entry_points={'console_scripts': ['iscan=iscan.scan:main']},
    python_requires='>=3.5',
    extras_require=EXTRAS_REQUIRE,
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
