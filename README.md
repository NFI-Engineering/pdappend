![Python package](https://github.com/chrispryer/pdappend/workflows/Python%20package/badge.svg)

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
