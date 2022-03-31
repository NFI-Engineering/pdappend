import os

import pandas as pd
import polars as pl
import polarsbear as pb


def clear() -> None:
    if os.path.exists(".pbappend"):
        os.remove(".pbappend")
    if os.path.exists("pbappend.csv"):
        os.remove("pbappend.csv")


test_dir = os.path.dirname(os.path.abspath(__file__))

# testing files
f1 = pb.read_csv(os.path.join(test_dir, "f1.csv"))
f2 = pb.read_csv(os.path.join(test_dir, "f2.csv"))
f3 = pl.from_pandas(
    pd.read_excel(os.path.join(test_dir, "f3.xls"), skiprows=[0])
)
f4 = pl.from_pandas(
    pd.read_excel(os.path.join(test_dir, "f4.xls"), skiprows=[0])
)
