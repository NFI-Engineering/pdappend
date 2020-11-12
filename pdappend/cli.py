import pandas as pd
import os
import logging
from dotenv import load_dotenv
from argparse import ArgumentParser
from collections import namedtuple

Args = namedtuple("args", ["dir", "sheet_name", "header_row"])


def is_filetype(filename: str) -> bool:
    """
    Return true if fname is ends with .csv, .xlsx, or .xls.
    Otherwise return False.

    :filename:      filename string

    Returns bool
    """
    cfname = filename.lower()

    if cfname.endswith(".csv"):
        return True

    elif cfname.endswith(".xlsx"):
        return True

    elif cfname.endswith(".xls"):
        return True

    logging.warning(f"file {filename} is not .csv, .xslx, or .xls")

    return False


def pd_read_file(
    fpath: str, sheet_name: str = None, header_index: int = None
) -> pd.DataFrame:
    """
    Read .csv, .xlsx, .xls to pandas dataframe. Read only a certain sheet name and skip
    to header row using sheet_name and header_index.

    :fpath:         path to file (str)
    :sheet_name:    sheet name to parse (str)
    :header_index:  index corresponding to header row of file (int)

    Returns DataFrame
    """
    cbasename = os.path.basename(fpath).lower()
    skiprows = []

    if cbasename == "pdappend.csv":
        return pd.DataFrame()

    if header_index:
        skiprows = list(range(0, int(header_index)))

    if not is_filetype(cbasename):
        raise ValueError(f"file {cbasename} is not .csv, .xslx, or .xls")

    if ".xls" in cbasename:
        return pd.read_excel(fpath, sheet_name=sheet_name, skiprows=skiprows)
    elif ".csv" in cbasename:
        return pd.read_csv(fpath, skiprows=skiprows)


def init_argparser(cwd: str) -> ArgumentParser:
    """
    Returns argparse.ArgumentParser with the following arguments:
    ~dir~:            relative filepath i.e. pdappend dir
    ~--sheet-name~:   string of excel sheet name i.e. "Sheet1"
    ~--header-row~:   integer of header row index (0 for first, 1 for second)

    :cwd:             current working dir string

    Returns argparse.ArgumentParser
    """

    def relative_path_to_absolute(relpath: str) -> str:
        return os.path.normpath(os.path.join(cwd, relpath))

    parser = ArgumentParser()
    parser.add_argument("dir", nargs="?", type=relative_path_to_absolute, default=cwd)
    # parser.add_argument("--to-excel", action="store_true")
    # parser.add_argument("--keep-row-index", action="store_true")
    parser.add_argument("--sheet-name", type=str)
    parser.add_argument("--header-row", type=int)
    # parser.add_argument("--no-filenames", action="store_true")
    # parser.add_argument("--only-common", action="store_true")

    return parser


def save_df(df: pd.DataFrame, _dir: str) -> None:
    """
    Saves pandas dataframe as pdappend.csv in a directory.

    :df:     pandas dataframe of data
    :dir:    string of full path to directory
    """
    fiilepath = os.path.join(_dir, "pdappend.csv")

    if os.path.exists(fiilepath):
        os.remove(fiilepath)

    df.to_csv(fiilepath, index=False)


def init_cli() -> Args:  # TODO: better return typing
    """
    Return commands from current working directory

    Returns Args
    """
    cwd = os.getcwd()
    cmd = init_argparser(cwd).parse_args()

    return cmd


def update_args_with_cli(args: Args, cli: Args) -> Args:
    """
    Updates args where a required field is not given using
    commands from cli. This prioritizes external args over cli.

    :args:      Args of dir, sheet_name, header_row
    :cli:       Args of dir, sheet_name, header_row

    Returns Args
    """
    if not args and cli:
        return cli

    if not cli and args:
        return args

    return Args(
        dir=args.dir or cli.dir or None,
        sheet_name=args.sheet_name or cli.sheet_name or None,
        header_row=args.header_row or cli.header_row or None,
    )


def main(args: Args = None):

    # pull commands from cli
    cmd = init_cli()
    args = update_args_with_cli(args, cli=cmd)

    load_dotenv(os.path.join(args.dir, ".pdappend"))

    # load
    files = [_ for _ in os.listdir(args.dir) if is_filetype(_)]
    sheet_name = os.getenv("SHEET_NAME") or args.sheet_name
    header_index = os.getenv("HEADER_ROW") or args.header_row

    # append
    df = pd.DataFrame()
    for fname in files:
        tmpdf = pd_read_file(os.path.join(args.dir, fname), sheet_name, header_index)
        tmpdf["filename"] = fname

        df = df.append(tmpdf, sort=False)

    save_df(df, _dir=args.dir)
