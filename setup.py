import setuptools

import iscan


with open('README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()


EXTRAS_REQUIRE = {
    'build': ['setuptools', 'twine', 'wheel'],
    'qa': ['flake8', 'isort', 'pre-commit'],
    'test': ['coverage', 'mypy', 'pytest'],
    'util': ['beautifulsoup4', 'requests']  # To scrape standard library modules
}
EXTRAS_REQUIRE['dev'] = EXTRAS_REQUIRE['build'] + EXTRAS_REQUIRE['qa'] + EXTRAS_REQUIRE['test'] + EXTRAS_REQUIRE['util']


setuptools.setup(
    name='iscan',
    version=iscan.__version__,
    url='https://github.com/zzhengnan/iscan',
    author='Zhengnan Zhao',
    description="iscan helps you identify your project's dependencies",
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    entry_points={'console_scripts': ['iscan=iscan.scan:main']},
    python_requires='>=3.7',
    extras_require=EXTRAS_REQUIRE,
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
