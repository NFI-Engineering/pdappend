import pdappend
import pandas as pd
import os
from . import test_dir, f1, f2, f3, f4


def init():
    os.chdir(test_dir)
    os.system("rm pdappend.csv .pdappend")


def get_result() -> pd.DataFrame:
    filepath = os.path.join(test_dir, "pdappend.csv")

    return pd.read_csv(filepath)


def write_pdappend_file():
    filepath = os.path.join(os.getcwd(), ".pdappend")

    with open(filepath, "w") as f:
        f.write(f"SHEET_NAME=Sheet1\nHEADER_ROW=1\nCSV_HEADER_ROW=0")

def teardown():
    os.system("rm .pdappend pdappend.csv")


def test_append_all():
    init()

    os.system("pdappend . --excel-header-row=1")

    result = get_result()

    assert result.shape[0] == f1.shape[0] + f2.shape[0] + f3.shape[0] + f4.shape[0]

    assert (
        result.shape[1] - 1 == f1.shape[1] == f2.shape[1] == f3.shape[1] == f4.shape[1]
    )


def test_append_filenames():
    init()

    os.system("pdappend f1.csv f4.xls --excel-header-row=1")

    result = get_result()

    assert result.shape[0] == f1.shape[0] + f4.shape[0]

    assert result.shape[1] - 1 == f1.shape[1] == f4.shape[1]

    teardown()


def test_append_wildcard():
    init()

    os.system("pdappend *.csv *.xls --excel-header-row=1")

    result = get_result()

    assert result.shape[0] == f1.shape[0] + f2.shape[0] + f3.shape[0] + f4.shape[0]

    assert (
        result.shape[1] - 1 == f1.shape[1] == f2.shape[1] == f3.shape[1] == f4.shape[1]
    )

    teardown()


def test_append_with_pdappend_file():
    init()
    write_pdappend_file()

    os.system("pdappend .")

    result = get_result()

    assert result.shape[0] == f1.shape[0] + f2.shape[0] + f3.shape[0] + f4.shape[0]

    assert (
        result.shape[1] - 1 == f1.shape[1] == f2.shape[1] == f3.shape[1] == f4.shape[1]
    )

    teardown()


def test_append_with_flags():
    init()

    os.system("pdappend . --sheet-name=Sheet1 --header-row=1 --csv-header-row=0")

    result = get_result()

    assert result.shape[0] == f1.shape[0] + f2.shape[0] + f3.shape[0] + f4.shape[0]

    assert (
        result.shape[1] - 1 == f1.shape[1] == f2.shape[1] == f3.shape[1] == f4.shape[1]
    )

    teardown()