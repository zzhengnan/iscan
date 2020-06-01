import setuptools


setuptools.setup(
    name='iscan',
    version='0.2.0',
    author='Zhengnan Zhao',
    description='iscan helps you identify your project\'s direct dependencies',
    url='https://github.com/ZhengnanZhao/iscan',
    packages=setuptools.find_packages(),
    extras_require={
        'dev': ['pytest', 'setuptools', 'twine', 'wheel']
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
