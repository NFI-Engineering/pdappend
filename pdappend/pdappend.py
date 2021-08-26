import os
import pandas as pd
import logging

from typing import NamedTuple, Union, Optional, List

from pdappend import utils
from pdappend.config import Config


FILETYPES = ["csv", "xls", "xlsx"]
DEFAULT_CONFIG = Config(
    sheet_name="Sheet1",
    header_row=0,
    excel_header_row=None,
    csv_header_row=None,
    save_as="csv",
    show=False,
)


class Targets(NamedTuple):
    values: Optional[Union[str, List[str]]]

    def __str__(self) -> str:
        return ", ".join([f"values: {self.values}"])


class Args(NamedTuple):
    targets: Targets
    flags: Config

    def __str__(self) -> str:
        return ", ".join([f"targets: {str(self.targets)}", f"flags: {str(self.flags)}"])


def is_filetype(filename: str) -> bool:
    """
    Return true if fname is ends with .csv, .xlsx, or .xls.
    Otherwise return False.

    :filename:      filename string

    Returns bool
    """
    cfname = filename.lower()

    if cfname.endswith(".csv") and not cfname.startswith("pdappend"):
        return True

    elif cfname.endswith(".xlsx"):
        return True

    elif cfname.endswith(".xls"):
        return True

    return False


def read_file(filepath: str, config: Config = DEFAULT_CONFIG) -> pd.DataFrame:
    """
    Read .csv, .xlsx, .xls to pandas dataframe. Read only a certain sheet name and skip
    to header row using sheet_name and header_index.

    :filepath:      path to file (str)
    :config:        dtype.Config

    Returns pd.DataFrame
    """
    filename = os.path.basename(filepath).lower()
    excel_header_row = utils._or(config.excel_header_row, config.header_row)
    csv_header_row = utils._or(config.csv_header_row, config.header_row)

    if filename == "pdappend.csv":
        logging.warning("Cannot read reserved result filename (pdappend.csv)")

        return pd.DataFrame()

    if not is_filetype(filename):
        raise ValueError(f"file {filename} is not .csv, .xslx, or .xls")

    if ".xls" in filename:
        return pd.read_excel(
            filepath,
            sheet_name=config.sheet_name,
            skiprows=list(range(0, int(excel_header_row))),
        )

    if filename.endswith(".csv"):
        return pd.read_csv(filepath, skiprows=list(range(0, int(csv_header_row))))


def append(files: List[str], config: Config = DEFAULT_CONFIG) -> pd.DataFrame:
    """
    Append files using pdappend.Config

    :files:     list of filepaths to read and append together
    :config:    pdappend.Config

    Returns pd.DataFrame
    """
    df = pd.DataFrame()

    for _ in files:
        logging.info(f"Appending {_}") if config.show else None
        tmpdf = read_file(_, config)
        tmpdf["filename"] = os.path.basename(_)

        df = df.append(tmpdf, sort=False)

    return df


def save_result(
    df: pd.DataFrame,
    save_as: str = DEFAULT_CONFIG.save_as,
    directory: str = os.getcwd(),
) -> None:
    """
    Saves pandas dataframe as pdappend.csv in a directory.

    :df:           pandas dataframe of data
    :save_as:      Config.save_as ("xls", "xlsx", "csv", "excel")
    :directory:    string of full path to directory
    """
    filepath = os.path.join(directory, f"pdappend.{save_as}")

    if os.path.exists(filepath):
        os.remove(filepath)

    if save_as == "xlsx":
        df.to_excel(filepath, index=False)

        return

    logging.info(
        f"Saving appended data ({df.shape[0]} rows, {df.shape[1]} columns) to {filepath}"
    )
    df.to_csv(filepath, index=False)
