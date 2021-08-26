from typing import NamedTuple

from pdappend import utils


class Config(NamedTuple):
    sheet_name: str
    header_row: int
    excel_header_row: int
    csv_header_row: int
    save_as: str
    show: bool

    def __str__(self) -> str:
        return ", ".join(
            [
                f"sheet_name: {self.sheet_name}",
                f"header_row: {self.header_row}",
                f"excel_header_row: {self.excel_header_row}",
                f"csv_header_row: {self.csv_header_row}",
                f"save_as: {self.save_as}",
                f"show: {self.show}",
            ]
        )

    def as_config_file(self) -> str:
        return "\n".join(
            [
                f"SHEET_NAME={self.sheet_name}",
                f"HEADER_ROW={self.header_row}",
                f"EXCEL_HEADER_ROW={utils._or(self.excel_header_row, '')}",
                f"CSV_HEADER_ROW={utils._or(self.csv_header_row, '')}",
                f"SAVE_AS={self.save_as}",
            ]
        )
