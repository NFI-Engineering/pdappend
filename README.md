[![PyPI Latest Release](https://img.shields.io/pypi/v/pbappend)](https://pypi.org/project/pbappend/)
![tests](https://github.com/cnpryer/pbappend/workflows/ci/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![pbappend](https://img.shields.io/pypi/pyversions/pbappend?color=blue)

This project is under development.

# pbappend

Run `pbappend` from the command line to append csv, xlsx, and xls files.

## Installation

`pip install pbappend`

## Using `pbappend`

Append specific files

`pbappend file1.csv file2.csv file3.csv`

Append specific file types in your directory

`pbappend *.csv`

Append all `pbappend`-compatible files in your directory

`pbappend .`

## Supported file types

- csv
- xls
- xlsx: [Not supported in Python 3.6 environments](https://groups.google.com/g/python-excel/c/IRa8IWq_4zk/m/Af8-hrRnAgAJ?pli=1) (downgrade to `xlrd 1.2.0` or convert to `.xls`)

## Documentation

(TODO)
See the [wiki](https://github.com/cnpryer/pbappend/wiki) for more on `pbappend`.

## Contributing

Pull requests are welcome!
