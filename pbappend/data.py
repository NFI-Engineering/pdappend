from enum import Enum


class FileExtension(str, Enum):
    """File extension data."""

    Csv = ".csv"
    Xls = ".xls"
    Xlsx = ".xlsx"
