from setuptools import setup, find_packages
from pdappend import __version__


long_description = ""
with open("./README.md") as f:
    long_description = f.read()

install_requires = []
with open("./requirements.txt") as f:
    install_requires = f.read().splitlines()

setup(
    name="pdappend",
    version=__version__,
    description="CLI package to append csv, xlsx, and xls files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chrispryer/pdappend",
    author="Chris Pryer",
    author_email="christophpryer@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "pdappend = pdappend.cli:main",
            "pdappend-gui = pdappend.gui:main",
        ]
    },
    zip_safe=False,
)
