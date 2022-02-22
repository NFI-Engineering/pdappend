[![PyPI Latest Release](https://img.shields.io/pypi/v/pdappend)](https://pypi.org/project/pdappend/)
![tests](https://github.com/cnpryer/pdappend/workflows/ci/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![pdappend](https://img.shields.io/pypi/pyversions/pdappend?color=blue)

This project is under development.

# pdappend

Run `pdappend` from the command line to append csv, xlsx, and xls files.

## Installation

`pip install pdappend`

## Using `pdappend`

Append specific files

`pdappend file1.csv file2.csv file3.csv`

Append specific file types in your directory

`pdappend *.csv`

Append all `pdappend`-compatible files in your directory

`pdappend .`

## Supported file types

- csv
- xls
- xlsx: [Not supported in Python 3.6 environments](https://groups.google.com/g/python-excel/c/IRa8IWq_4zk/m/Af8-hrRnAgAJ?pli=1) (downgrade to `xlrd 1.2.0` or convert to `.xls`)

## Documentation

(TODO)
See the [wiki](https://github.com/cnpryer/pdappend/wiki) for more on `pdappend`.

## Contributing

Pull requests are welcome!
