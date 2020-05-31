import setuptools


setuptools.setup(
    name="iscan",
    version="0.1.0",
    author="Zhengnan Zhao",
    description="iscan aggregates your project's direct dependencies",
    url="https://github.com/ZhengnanZhao/iscan",
    packages=setuptools.find_packages(),
    extras_require={
        "dev": ["pytest", "setuptools", "twine", "wheel"]
    },
    entry_points={'console_scripts': ['iscan=iscan.scan:main']}
)
