import os

import polarsbear as pb
from click.testing import CliRunner

from pbappend import cli

from . import clear, f1, f2, f3, f4

# clear testing artifacts TODO: pytest tmp dirs
clear()

runner = CliRunner()


def get_result_file() -> pb.DataFrame:
    filepath = "pbappend.csv"

    if not os.path.exists(filepath):
        return pb.DataFrame()

    return pb.read_csv(filepath)


def write_pbappend_file() -> None:
    filepath = os.path.join(os.getcwd(), ".pbappend")

    with open(filepath, "w") as f:
        f.write(
            "SHEET_NAME=Sheet1\nCSV_HEADER_ROW=0\nEXCEL_HEADER_ROW=1\n"
            "SAVE_AS=.csv\nRECURSIVE=True"
            "\nIGNORE=.venv,dist,.pytest_cache,__pycache__,.git"
        )


def test_append_all():
    clear()

    res = runner.invoke(
        cli.main,
        [
            ".",
            "--excel-header-row=1",
            "--recursive",
            "--ignore=.venv",
            "--ignore=dist",
            "--ignore=.pytest_cache",
            "--ignore=__pycache__",
            "--ignore=.git",
        ],
    )

    assert res.exit_code == 0

    res = get_result_file()

    assert (
        res.shape[0] == f1.shape[0] + f2.shape[0] + f3.shape[0] + f4.shape[0]
    )

    assert (
        res.shape[1] - 1
        == f1.shape[1]
        == f2.shape[1]
        == f3.shape[1]
        == f4.shape[1]
    )


def test_append_filenames():
    clear()

    res = runner.invoke(
        cli.main,
        [
            "f1.csv",
            "f4.xls",
            "--excel-header-row=1",
            "--recursive",
            "--ignore=.venv",
            "--ignore=dist",
            "--ignore=.pytest_cache",
            "--ignore=__pycache__",
            "--ignore=.git",
        ],
    )

    assert res.exit_code == 0

    res = get_result_file()

    assert res.shape[0] == f1.shape[0] + f4.shape[0]

    assert res.shape[1] - 1 == f1.shape[1] == f4.shape[1]


def test_append_wildcard():
    clear()

    res = runner.invoke(
        cli.main,
        [
            "*.csv",
            "*.xls",
            "--excel-header-row=1",
            "--recursive",
            "--ignore=.venv",
            "--ignore=dist",
            "--ignore=.pytest_cache",
            "--ignore=__pycache__",
            "--ignore=.git",
        ],
    )

    assert res.exit_code == 0

    res = get_result_file()

    assert (
        res.shape[0] == f1.shape[0] + f2.shape[0] + f3.shape[0] + f4.shape[0]
    )

    assert (
        res.shape[1] - 1
        == f1.shape[1]
        == f2.shape[1]
        == f3.shape[1]
        == f4.shape[1]
    )


def test_append_with_pbappend_file():
    clear()
    write_pbappend_file()

    res = runner.invoke(
        cli.main,
        [
            ".",
            "--recursive",
            "--ignore=.venv",
            "--ignore=dist",
            "--ignore=.pytest_cache",
            "--ignore=__pycache__",
            "--ignore=.git",
        ],
    )

    assert res.exit_code == 0

    res = get_result_file()

    assert (
        res.shape[0] == f1.shape[0] + f2.shape[0] + f3.shape[0] + f4.shape[0]
    )

    assert (
        res.shape[1] - 1
        == f1.shape[1]
        == f2.shape[1]
        == f3.shape[1]
        == f4.shape[1]
    )


def test_append_with_flags():
    clear()

    res = runner.invoke(
        cli.main,
        [
            ".",
            "--sheet-name=Sheet1",
            "--csv-header-row=0",
            "--excel-header-row=1",
            "--recursive",
            "--ignore=.venv",
            "--ignore=dist",
            "--ignore=.pytest_cache",
            "--ignore=__pycache__",
            "--ignore=.git",
        ],
    )

    assert res.exit_code == 0

    res = get_result_file()

    assert (
        res.shape[0] == f1.shape[0] + f2.shape[0] + f3.shape[0] + f4.shape[0]
    )

    assert (
        res.shape[1] - 1
        == f1.shape[1]
        == f2.shape[1]
        == f3.shape[1]
        == f4.shape[1]
    )
