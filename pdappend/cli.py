import pandas as pd
import os
import logging
from dotenv import load_dotenv


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


def pd_read_file(fpath: str, sheet_name: str=None, header_index: int=None) -> pd.DataFrame:
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

    if header_index:
        skiprows = list(range(0, int(header_index)))

    if not is_filetype(cbasename):
        raise ValueError(f"file {cbasename} is not .csv, .xslx, or .xls")

    if ".xls" in cbasename:
        return pd.read_excel(fpath, sheet_name=sheet_name, skiprows=skiprows)
    elif ".csv" in cbasename:
        return pd.read_csv(fpath, skiprows=skiprows)


def main():
    cur_dir = os.getcwd()
    load_dotenv(os.path.join(cur_dir, ".pdappend"))
    sheet_name = os.getenv("SHEET_NAME") or None
    header_index = os.getenv("HEADER_ROW") or None
    logging.debug(f".pdappend SHEET_NAME: {sheet_name}")

    files = [_ for _ in os.listdir(cur_dir) if is_filetype(_)]

    df = pd.DataFrame()
    for fname in files:
        tmpdf = pd_read_file(os.path.join(cur_dir, fname), sheet_name, header_index)
        tmpdf["filename"] = fname

        df = df.append(tmpdf, sort=False)

    df.to_csv(os.path.join(cur_dir, "pdappend.csv"), index=False)
