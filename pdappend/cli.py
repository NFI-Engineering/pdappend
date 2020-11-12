import pandas as pd
import os
import logging
from dotenv import load_dotenv
from argparse import ArgumentParser


def is_filetype(fname: str) -> bool:
    cfname = fname.lower()

    if cfname.endswith(".csv"):
        return True
    elif cfname.endswith(".xlsx"):
        return True
    elif cfname.endswith(".xls"):
        return True
    else:
        logging.warning(f"file {fname} is not .csv, .xslx, or .xls")


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
    def relative_path_to_absolute(relpath: str) -> str:
        return os.path.normpath(os.path.join(cwd, relpath))

    parser = ArgumentParser()
    parser.add_argument("dir", nargs="?", type=relative_path_to_absolute, default=cwd)
    parser.add_argument("--to-excel", action="store_true")
    parser.add_argument("--keep-row-index", action="store_true")
    parser.add_argument("--sheet-name", type=str)
    parser.add_argument("--header-row", type=int)
    parser.add_argument("--no-filenames", action="store_true")
    parser.add_argument("--only-common", action="store_true")

    return parser


def save_df(df: pd.DataFrame, dir: str) -> None:
    rpath = os.path.join(dir, "pdappend.csv")

    if os.path.exists(rpath):
        os.remove(rpath)

    df.to_csv(rpath, index=False)


def main(args: list = None):
    cwd = os.getcwd()

    if not args:
        args = init_argparser(cwd).parse_args()

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

    save_df(df=df, dir=args.dir)
