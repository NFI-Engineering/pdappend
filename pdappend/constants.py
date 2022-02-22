from pdappend.data import FileExtension


CSV_HEADER_ROW_DESCRIPTION = "Integer position of header row in .csv files."
DEFAULT_CSV_HEADER_ROW = 0

EXCEL_HEADER_ROW_DESCRIPTION = (
    "Integer position of header row in .xls and .xslx files."
)
DEFAULT_EXCEL_HEADER_ROW = 0

SAVE_AS_DESCRIPTION = "File extention type to save result as."
DEFAULT_SAVE_AS = FileExtension.Csv.value

SHEET_NAME_DESCRIPTION = "Sheet name in Excel files to target."
DEFAULT_SHEET_NAME = "Sheet1"
