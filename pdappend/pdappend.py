import os
import pandas as pd
import click

from typing import NamedTuple, List, Tuple, Union
from dotenv import load_dotenv

from pdappend import constants
from pdappend.errors import FileExtensionError, SaveAsError
from pdappend.data import FileExtension


# file extension types pdappend recognizes and can consume
FILE_EXTENSIONS_ALLOWED = [
    FileExtension.Csv,
    FileExtension.Xls,
    FileExtension.Xlsx,
]

# possible filenames for results
RESULT_FILENAMES_ALLOWED = [
    f"pdappend{_.value}" for _ in FILE_EXTENSIONS_ALLOWED
]


class Config(NamedTuple):
    """pdappend Config data."""

    sheet_name: str = constants.DEFAULT_SHEET_NAME
    csv_header_row: int = constants.DEFAULT_CSV_HEADER_ROW
    excel_header_row: int = constants.DEFAULT_EXCEL_HEADER_ROW
    save_as: str = constants.DEFAULT_SAVE_AS
    verbose: bool = constants.DEFAULT_VERBOSE
    recursive: bool = constants.DEFAULT_VERBOSE
    ignore: Union[List[str], Tuple[str]] = constants.DEFAULT_IGNORE

    def __str__(self) -> str:
        return ", ".join(
            [
                f"sheet_name: {self.sheet_name}",
                f"excel_header_row: {self.excel_header_row}",
                f"csv_header_row: {self.csv_header_row}",
                f"save_as: {self.save_as}",
                f"verbose: {self.verbose}",
                f"recursive: {self.recursive}",
                f"ignore: {self.ignore}",
            ]
        )

    def as_config_file(self) -> str:
        ignore_str = str(self.ignore).replace("[", "").replace("[", "")

        return "\n".join(
            [
                f"SHEET_NAME={self.sheet_name}",
                f"EXCEL_HEADER_ROW={self.excel_header_row}",
                f"CSV_HEADER_ROW={self.csv_header_row}",
                f"SAVE_AS={self.save_as}",
                f"VERBOSE={self.verbose}",
                f"RECURSIVE={self.recursive}",
                f"IGNORE={ignore_str}",
            ]
        )


def read_pdappend_file() -> Config:
    """Init Args with .pdappend file. TODO: replace with `yml`"""
    load_dotenv(".pdappend")

    sheet_name = os.getenv("SHEET_NAME") or constants.DEFAULT_SHEET_NAME
    csv_header_row = (
        int(os.getenv("CSV_HEADER_ROW"))
        if os.getenv("CSV_HEADER_ROW")
        else constants.DEFAULT_CSV_HEADER_ROW
    )
    excel_header_row = (
        int(os.getenv("EXCEL_HEADER_ROW"))
        if os.getenv("EXCEL_HEADER_ROW")
        else constants.DEFAULT_EXCEL_HEADER_ROW
    )
    save_as = os.getenv("SAVE_AS") or constants.DEFAULT_SAVE_AS
    verbose = True if os.getenv("VERBOSE") in ["1", "True"] else False
    recursive = True if os.getenv("RECURSIVE") in ["1", "True"] else False
    ignore = (
        os.getenv("IGNORE").split(",")
        if os.getenv("IGNORE")
        else constants.DEFAULT_IGNORE
    )
    ignore = [_.strip() for _ in ignore]

    config = Config(
        sheet_name,
        csv_header_row,
        excel_header_row,
        save_as,
        verbose,
        recursive,
        ignore,
    )

    return config


def parse_filename_extension(filename: str) -> FileExtension:
    """Parses FileExtension from filename.

    Args:
        filename (str): String of filename to parse.

    Returns:
        FileExtension: FileExtension data.
    """
    ext = os.path.splitext(filename)[1]

    return ext


def read_file(filepath: str, config: Config = Config()) -> pd.DataFrame:
    """Read .csv, .xlsx, .xls to pandas dataframe. Read only a certain sheet
    name and skip to header row using sheet_name and header_index.

    Args:
        filepath (str): Path to file.
        config (Config, optional): dtype.Config.

    Raises:
        FileExtensionError: Error if filetype is incorrect.

    Returns:
        pd.DataFrame: Pandas DataFrame.
    """
    filename = os.path.basename(filepath).lower()
    ext = parse_filename_extension(filename)

    if filename in RESULT_FILENAMES_ALLOWED:
        click.echo(
            f"WARNING: Cannot read reserved result filename ({filename})"
        )

        return pd.DataFrame()

    if ext not in FILE_EXTENSIONS_ALLOWED:
        raise FileExtensionError(
            f"File {filename} is not {FILE_EXTENSIONS_ALLOWED}"
        )

    if ext == FileExtension.Xlsx or ext == FileExtension.Xls:
        df = pd.read_excel(
            filepath,
            sheet_name=config.sheet_name,
            skiprows=list(range(0, config.excel_header_row)),
        )

        return df

    if ext == FileExtension.Csv:
        df = pd.read_csv(
            filepath, skiprows=list(range(0, config.csv_header_row))
        )

        return df


def append(
    files: Union[List[str], Tuple[str]], config: Config = Config()
) -> pd.DataFrame:
    """Append files using pdappend.Config.

    Args:
        files (List[str]): list of filepaths to read and append together.
        config (Config, optional): pdappend.Config. Defaults to DEFAULT_CONFIG.

    Returns:
        pd.DataFrame: Appended Pandas DataFrame.
    """
    targets = []
    for _ in files:
        click.echo(f"Appending {_}") if config.verbose else None
        target_df = read_file(_, config)
        target_df["filename"] = os.path.basename(_)
        targets.append(target_df)

    df = pd.concat(targets)

    return df


def save_result(
    df: pd.DataFrame,
    config: Config = Config(),
    directory: str = os.getcwd(),
) -> None:
    """Saves Pandas DataFrame as pdappend{Config.save_as} in a directory.

    Args:
        df (pd.DataFrame): Pandas DataFrame.
        config (Config, optional): pdappend Config. Defaults to Config().
        directory (str, optional): String of full path to directory. Defaults
        to os.getcwd().

    Raises:
        SaveAsError: Save-as data is invalid.
    """
    # TODO: force full dot-string extension
    ext = (
        config.save_as
        if config.save_as.startswith(".")
        else "." + config.save_as
    )
    filepath = os.path.join(
        directory,
        f"pdappend{ext}",
    )

    if os.path.exists(filepath):
        os.remove(filepath)

    if config.verbose:
        click.echo(
            "Saving appended data "
            f"({df.shape[0]} rows, {df.shape[1]} columns) to {filepath}"
        )

    if (
        config.save_as == FileExtension.Xlsx
        or config.save_as == FileExtension.Xls
    ):
        df.to_excel(filepath, index=False)

        return

    if config.save_as == FileExtension.Csv:
        df.to_csv(filepath, index=False)

        return

    raise SaveAsError(f"Could not save file as {config.save_as}.")
