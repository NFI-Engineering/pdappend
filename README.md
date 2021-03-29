[![PyPI Latest Release](https://img.shields.io/pypi/v/pdappend)](https://pypi.org/project/pdappend/)
![Python package](https://github.com/cnpls/pdappend/workflows/Tests/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![pdappend](https://img.shields.io/pypi/pyversions/pdappend?color=blue)

# pdappend

Run `pdappend` from the command line to append csv, xlsx, and xls files. 

## Installation

`pip install pdappend`

## Using `pdappend`

`pdappend file1.csv file2.csv file3.csv` or `pdappend *.csv` to append all `.csv` files in the current directory. `pdappend .` will search for all compatible file types and append them.

## Supported file types

- csv
- xls
- xlsx: [Not supported in Python 3.6 environments](https://groups.google.com/g/python-excel/c/IRa8IWq_4zk/m/Af8-hrRnAgAJ?pli=1) (downgrade to `xlrd 1.2.0` or convert to `.xls`)

## For specific sheets in Excel files

### Using the command line

Use the flag `--sheet-name` to add a specific sheet name. For example: `pdappend *.xls --sheet-name="Sheet Name"`.

### Using `.pdappend` files

In the current working directory add a `.pdappend` file containing:
```.env
SHEET_NAME=Sheet Name
```

## `pdappend-gui`

Run `pdappend-gui` at the command line to select files manually. You use the same flags and `.pdappend` configs for this method as well.

## Header row configuration

If the first row of your Excel sheet is not the column row use the `--header-row` flag or `HEADER_ROW` in the `.pdappend` to add the column row number. The default header row is 0.