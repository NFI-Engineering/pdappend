import io
import os
import re

from setuptools import setup, find_packages


CLASSIFIERS = """\
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Topic :: Software Development
Operating System :: Microsoft :: Windows
Operating System :: Unix
Operating System :: MacOS

"""


# https://packaging.python.org/guides/single-sourcing-package-version/
def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8"),
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)


project_root = os.path.dirname(os.path.abspath(__file__))

long_description = ""
with open(os.path.join(project_root, "README.md")) as f:
    long_description = f.read()

install_requires = []
with open(os.path.join(project_root, "requirements.txt")) as f:
    install_requires = f.read().splitlines()

setup(
    name="pdappend",
    version=find_version(os.path.join(project_root, "pdappend", "__init__.py")),
    description="Append csv, xlsx, and xls files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cnp0/pdappend",
    author="Chris Pryer",
    author_email="andromia.software@gmail.com",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "pdappend = pdappend.cli:main",
            "pdappend-gui = pdappend.gui:main",
        ]
    },
    classifiers=[_ for _ in CLASSIFIERS.split("\n") if _],
)
