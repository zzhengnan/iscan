import setuptools


setuptools.setup(
    name="importscanner",
    version="0.0.1",
    author="Zhengnan Zhao",
    description="importscanner helps identify your project's direct dependencies",
    url="https://github.com/ZhengnanZhao/importscanner",
    packages=setuptools.find_packages(),
    entry_points={'console_scripts': ['importscanner=importscanner.scan:main']}
)
