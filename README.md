[![PyPI Latest Release](https://img.shields.io/pypi/v/pdappend)](https://pypi.org/project/pdappend/)
![Python package](https://github.com/cnpls/pdappend/workflows/Python%20package/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# pdappend

Run `pdappend` in a directory to append together csv, xlsx, and xls files.

## Instructions

1. `pip install pdappend`
2. From inside the directory you'd like to append files together `pdappend`

### For specific sheets in Excel files

Before running `pdappend` add a `.pdappend` file to the directory you'd like to run it in. Configre the `.pdappend` with the sheet name you want to process and rows or columns you'd like to skip:

`.pdappend`
```.env
SHEET_NAME=Sheet Name
HEADER_ROW=1 # starts at 0, to skip first row use HEADER_ROW=1
```

### `pdappend-gui`

`pdappend-gui` comes packaged with `pdappend`. Run `pdappend-gui` at the command line to select a directory manually.


### More cli args

- `--sheet-name`: string
- `--header-row`: integer
