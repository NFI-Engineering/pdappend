import pandas as pd
import os
import logging
from dotenv import load_dotenv
from argparse import ArgumentParser
from typing import List, Optional, Union

from pdappend import pdappend, dtypes, utils


logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


DEFAULT_TARGETS = dtypes.Targets(values=".")
DEFAULT_ARGS = dtypes.Args(targets=DEFAULT_TARGETS, flags=pdappend.DEFAULT_CONFIG)


def update_targets(
    targets0: dtypes.Targets, targets1: dtypes.Targets
) -> dtypes.Targets:
    """
    Override default values from targets1 -> targets0 and return dtypes.Targets to use.

    :targets0:    dtypes.Targets to override
    :targets1:    dtypes.Targets to override targets0 with

    Returns dtypes.Targets
    """
    if targets0 == DEFAULT_TARGETS and targets1 != DEFAULT_TARGETS:
        return targets1

    if targets0 != DEFAULT_TARGETS and targets1 == DEFAULT_TARGETS:
        return targets0

    values = targets0.values

    # redundant without more Targets properties
    if targets0.values == DEFAULT_TARGETS.values:
        values = targets1.values

    targets = dtypes.Targets(values)

    return targets


def update_flags(flags0: dtypes.Config, flags1: dtypes.Config) -> dtypes.Config:
    """
    Override default values from flags1 -> flags0 and return dtypes.Config to use.

    :flags0:    dtypes.Flags to override
    :flags1:    dtypes.Flags to override flags0 with

    Returns dtypes.Config
    """
    if flags0 == pdappend.DEFAULT_CONFIG and flags1 != pdappend.DEFAULT_CONFIG:
        return flags1

    if flags0 != pdappend.DEFAULT_CONFIG and flags1 == pdappend.DEFAULT_CONFIG:
        return flags0

    sheet_name = flags0.sheet_name
    header_row = flags0.header_row
    excel_header_row = flags0.excel_header_row
    csv_header_row = flags0.csv_header_row
    save_as = flags0.save_as

    if flags0.sheet_name == pdappend.DEFAULT_CONFIG.sheet_name:
        sheet_name = flags1.sheet_name

    if flags0.header_row == pdappend.DEFAULT_CONFIG.header_row:
        header_row = flags1.header_row

    if flags0.excel_header_row == pdappend.DEFAULT_CONFIG.excel_header_row:
        excel_header_row = flags1.excel_header_row

    if flags0.csv_header_row == pdappend.DEFAULT_CONFIG.csv_header_row:
        csv_header_row = flags1.csv_header_row

    if flags0.save_as == pdappend.DEFAULT_CONFIG.save_as:
        save_as = flags1.save_as

    flags = dtypes.Config(
        sheet_name, header_row, excel_header_row, csv_header_row, save_as
    )

    return flags


def update_args(args0: dtypes.Args, args1: dtypes.Args) -> dtypes.Args:
    """
    Override default values from args1 -> args0 and return dtypes.Args to use.

    :args0:    dtypes.Args to override
    :args1:    dtypes.Args to override args0 with

    Returns dtypes.Args
    """
    if args0 == DEFAULT_ARGS and args1 != DEFAULT_ARGS:
        return args1

    if args0 != DEFAULT_ARGS and args1 == DEFAULT_ARGS:
        return args0

    targets = update_targets(targets0=args0.targets, targets1=args1.targets)
    flags = update_flags(flags0=args0.flags, flags1=args1.flags)

    return dtypes.Args(targets, flags)


def init_pdappend_file() -> dtypes.Args:
    cwd = os.getcwd()
    load_dotenv(os.path.join(cwd, ".pdappend"))

    targets = DEFAULT_TARGETS
    config = dtypes.Config(
        sheet_name=utils._or(
            os.getenv("SHEET_NAME"), pdappend.DEFAULT_CONFIG.sheet_name
        ),
        header_row=utils._or(
            os.getenv("HEADER_ROW"), pdappend.DEFAULT_CONFIG.header_row
        ),
        excel_header_row=utils._or(
            os.getenv("EXCEL_HEADER_ROW"), pdappend.DEFAULT_CONFIG.excel_header_row
        ),
        csv_header_row=utils._or(
            os.getenv("CSV_HEADER_ROW"), pdappend.DEFAULT_CONFIG.csv_header_row
        ),
        save_as=utils._or(os.getenv("SAVE_AS"), pdappend.DEFAULT_CONFIG.save_as),
    )

    args = dtypes.Args(targets, flags=config)

    return args


def create_pdappend_file() -> None:
    string = pdappend.DEFAULT_CONFIG.as_config_file()
    filepath = os.path.join(os.getcwd(), ".pdappend")

    with open(filepath, "w") as f:
        f.write(string)

    logging.info(f".pdappend file saved to {os.path.dirname(filepath)}")


def init_argparser() -> ArgumentParser:
    """
    Returns argparse.ArgumentParser with dtype.Args childrens' props in namespace

    Returns argparse.ArgumentParser
    """
    cwd = os.getcwd()

    def wildcard_to_filepaths(value: str) -> str:
        filepaths = [
            os.path.join(cwd, _)
            for _ in os.listdir(cwd)
            if _.endswith(value.replace("*", "")) and pdappend.is_filetype(_)
        ]

        return filepaths

    def target_to_filepath(target: str) -> Optional[Union[str, List[str]]]:
        if target == "setup":
            return target

        if target == ".":
            filepaths = [
                os.path.join(cwd, _) for _ in os.listdir(cwd) if pdappend.is_filetype(_)
            ]

            return filepaths

        ctarrget = target.lower().strip()

        if (
            os.path.basename(ctarrget).replace("*", "").replace(".", "")
            in dtypes.FILETYPES
        ):
            return wildcard_to_filepaths(target)

        filepath = os.path.normpath(os.path.join(cwd, target))

        return filepath

    def parse_save_as(string: str) -> str:
        cstring = string.lower().strip()

        if cstring not in dtypes.FILETYPES + ["excel"]:
            raise (
                ValueError(
                    f"save-as configuration ({string}) is not a recognized result file type"
                )
            )

        if cstring == "excel":
            return "xlsx"

        return cstring

    parser = ArgumentParser()
    parser.add_argument("targets", nargs="*", type=target_to_filepath, default=".")
    parser.add_argument(
        "--sheet-name", type=str, default=pdappend.DEFAULT_CONFIG.sheet_name
    )
    parser.add_argument(
        "--header-row", type=int, default=pdappend.DEFAULT_CONFIG.header_row
    )
    parser.add_argument(
        "--excel-header-row", type=int, default=pdappend.DEFAULT_CONFIG.excel_header_row
    )
    parser.add_argument(
        "--csv-header-row", type=int, default=pdappend.DEFAULT_CONFIG.csv_header_row
    )
    parser.add_argument(
        "--save-as", type=parse_save_as, default=pdappend.DEFAULT_CONFIG.save_as
    )

    return parser


def init_cli() -> dtypes.Args:
    """
    Return dtypes.Args using prioritized commands and secondary .pdappend

    Returns Args
    """
    pdappend_file_args = init_pdappend_file()
    parsed_args = init_argparser().parse_args()
    command_args = dtypes.Args(
        targets=dtypes.Targets(values=parsed_args.targets),
        flags=dtypes.Config(
            sheet_name=parsed_args.sheet_name,
            header_row=parsed_args.header_row,
            excel_header_row=parsed_args.excel_header_row,
            csv_header_row=parsed_args.csv_header_row,
            save_as=parsed_args.save_as,
        ),
    )

    args = update_args(args0=pdappend_file_args, args1=command_args)

    return args


def unpack_processed_targets(targets: List[str]) -> List[str]:
    unpacked_targets = [_ for _ in targets]

    return unpacked_targets


def main(external_args: dtypes.Args = DEFAULT_ARGS):
    initialized_args = init_cli()

    # override any default configuration from arg1 -> arg0
    args = update_args(args0=initialized_args, args1=external_args)

    if args.targets.values == ["setup"] or args.targets.values == "setup":
        create_pdappend_file()

        return

    logging.info(f"pdappend setup {str(args)}")

    files = []
    for _ in args.targets.values:
        if isinstance(_, list):
            files += unpack_processed_targets(_)
        else:
            files.append(_)

    files = list(set(files))
    df = pdappend.append(files, config=args.flags)
    pdappend.save_result(df, save_as=args.flags.save_as)
