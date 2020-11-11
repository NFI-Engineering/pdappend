![Python package](https://github.com/fingafrog/python-package/workflows/Python%20package/badge.svg)

# python-package

Template repository for building python packages and publishing to pypi.

## Instructions

1. Rename `package/`

2. Update `setup.py`

```python
from setuptools import setup, find_packages
from package import __version__ # rename package here


long_description = ''
with open('./README.md') as f:
    long_description = f.read()

install_requires = []
with open('./requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(name='package', # rename package here
    version=__version__,
    description='', # add a short description here
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='', # add your repository url here
    author='', # add your name here
    author_email='', # add your email here
    license='PUBLIC', # change to PRIVATE if you'd like
    packages=find_packages(),
    install_requires=install_requires,
    entry_points ={ # add an entry point for cli here
            'console_scripts': [
                'package = package.main:main' # rename package, point at a function
            ]
        },
    zip_safe=False)
```

3. [Update your status badge](https://docs.github.com/en/actions/configuring-and-managing-workflows/configuring-a-workflow#adding-a-workflow-status-badge-to-your-repository)

4. Update `README.md`

3. :rocket:
