![Python package](https://github.com/NFI-Engineering/pdappend/workflows/Python%20package/badge.svg)

# python-package

CLI package to append csv, xlsx, xls files.

## Instructions

1. `pip install pdappend`
2. From inside the directory you'd like to append files together `pdappend`

### For specific sheets in Excel files

Before running `pdappend` add a `.pdappend` file to the directory you'd like to run it in. Configre the `.pdappend` with the sheet name you want to process:

`.pdappend`

```.env
SHEET_NAME=Sheet Name
```
