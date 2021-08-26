import os
import sys
import logging

from dotenv import load_dotenv
from argparse import ArgumentParser

from typing import List, Optional, Union

from pdappend import pdappend, utils


DEFAULT_TARGETS = pdappend.Targets(values=".")
DEFAULT_ARGS = pdappend.Args(targets=DEFAULT_TARGETS, flags=pdappend.DEFAULT_CONFIG)


def init_logging() -> None:
    """cli.py module logging init function"""
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def merge_targets(
    targets0: pdappend.Targets, targets1: pdappend.Targets
) -> pdappend.Targets:
    """
    Override default values from targets1 -> targets0 and return pdappend.Targets to use.

    :targets0:    pdappend.Targets to override
    :targets1:    pdappend.Targets to override targets0 with

    Returns pdappend.Targets
    """
    if targets0 == DEFAULT_TARGETS and targets1 != DEFAULT_TARGETS:
        return targets1

    if targets0 != DEFAULT_TARGETS and targets1 == DEFAULT_TARGETS:
        return targets0

    values = targets0.values

    # redundant without more Targets properties
    if targets0.values == DEFAULT_TARGETS.values:
        values = targets1.values

    targets = pdappend.Targets(values)

    return targets


def merge_flags(flags0: pdappend.Config, flags1: pdappend.Config) -> pdappend.Config:
    """
    Override default values from flags1 -> flags0 and return pdappend.Config to use.

    :flags0:    pdappend.Flags to override
    :flags1:    pdappend.Flags to override flags0 with

    Returns pdappend.Config
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
    show = flags0.show

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

    if flags0.show == pdappend.DEFAULT_CONFIG.show:
        show = flags1.show

    flags = pdappend.Config(
        sheet_name, header_row, excel_header_row, csv_header_row, save_as, show
    )

    return flags


def merge_args(args0: pdappend.Args, args1: pdappend.Args) -> pdappend.Args:
    """
    Override default values from args1 -> args0 and return pdappend.Args to use.

    :args0:    pdappend.Args to override
    :args1:    pdappend.Args to override args0 with

    Returns pdappend.Args
    """
    if args0 == DEFAULT_ARGS and args1 != DEFAULT_ARGS:
        return args1

    if args0 != DEFAULT_ARGS and args1 == DEFAULT_ARGS:
        return args0

    targets = merge_targets(targets0=args0.targets, targets1=args1.targets)
    flags = merge_flags(flags0=args0.flags, flags1=args1.flags)

    return pdappend.Args(targets, flags)


def init_pdappend_file() -> pdappend.Args:
    load_dotenv(".pdappend")

    config = pdappend.Config(
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
        show=utils._or(
            utils.str_to_bool(os.getenv("SHOW")), pdappend.DEFAULT_CONFIG.show
        ),
    )

    args = pdappend.Args(targets=DEFAULT_TARGETS, flags=config)

    return args


def create_pdappend_file() -> None:
    """Create .pdappend file in current working directory"""
    string = pdappend.DEFAULT_CONFIG.as_config_file()
    filepath = os.path.join(os.getcwd(), ".pdappend")

    with open(filepath, "w") as f:
        f.write(string)

    logging.info(f".pdappend file saved to {os.path.dirname(filepath)}")


def init_argparser() -> ArgumentParser:
    """
    Returns argparse.ArgumentParser with dtype.Args childrens' props in namespace
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

        ctarget = target.lower().strip()

        if (
            os.path.basename(ctarget).replace("*", "").replace(".", "")
            in pdappend.FILETYPES
        ):
            return wildcard_to_filepaths(target)

        filepath = os.path.normpath(os.path.join(cwd, target))

        return filepath

    def parse_save_as(string: str) -> str:
        cstring = string.lower().strip()

        if cstring not in pdappend.FILETYPES + ["excel"]:
            raise (
                ValueError(
                    f"save-as configuration ({string}) is not a recognized result file type"
                )
            )

        if cstring == "excel":
            return "xlsx"

        return cstring

    parser = ArgumentParser(description="pdappend csv, xlsx, and xls files.")
    parser.add_argument(
        "targets",
        nargs="*",
        type=target_to_filepath,
        help="files to append ('.', 'file.csv', '*.csv')",
    )
    parser.add_argument(
        "--sheet-name",
        type=str,
        default=pdappend.DEFAULT_CONFIG.sheet_name,
        help="Sheet name in excel files (default is 'Sheet1')",
    )
    parser.add_argument(
        "--header-row",
        type=int,
        default=pdappend.DEFAULT_CONFIG.header_row,
        help="Row number of column row (default is 0)",
    )
    parser.add_argument(
        "--excel-header-row",
        type=int,
        default=pdappend.DEFAULT_CONFIG.excel_header_row,
        help="Row number of column row in excel files (default is --header-row or 0)",
    )
    parser.add_argument(
        "--csv-header-row",
        type=int,
        default=pdappend.DEFAULT_CONFIG.csv_header_row,
        help="Row number of column row in csv files (default is --header-row or 0)",
    )
    parser.add_argument(
        "--save-as",
        type=parse_save_as,
        default=pdappend.DEFAULT_CONFIG.save_as,
        help="File type to save appended results as ('csv', 'xlsx', 'xls', 'excel')",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Print files being appended",
    )

    return parser


def init_cli() -> pdappend.Args:
    """
    Return pdappend.Args using prioritized commands and secondary .pdappend
    """
    pdappend_file_args = init_pdappend_file()
    parsed_args = init_argparser().parse_args()
    command_args = pdappend.Args(
        targets=pdappend.Targets(values=parsed_args.targets),
        flags=pdappend.Config(
            sheet_name=parsed_args.sheet_name,
            header_row=parsed_args.header_row,
            excel_header_row=parsed_args.excel_header_row,
            csv_header_row=parsed_args.csv_header_row,
            save_as=parsed_args.save_as,
            show=parsed_args.show,
        ),
    )

    args = merge_args(args0=pdappend_file_args, args1=command_args)

    return args


def unpack_processed_targets(targets: List[str]) -> List[str]:
    unpacked_targets = [_ for _ in targets]

    return unpacked_targets


def main(external_args: pdappend.Args = DEFAULT_ARGS):
    init_logging()
    initialized_args = init_cli()

    # override any default configuration from arg1 -> arg0
    args = merge_args(args0=initialized_args, args1=external_args)

    if args.targets.values == ["setup"] or args.targets.values == "setup":
        create_pdappend_file()

        return

    if len(sys.argv) == 1:
        print(
            "\n".join(
                [
                    "",
                    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
                    "~~~~~~~~~~ Welcome to pdappend! ~~~~~~~~~~~",
                    "",
                    "Use pdappend to append csv, xlsx, and xls files.",
                    "If you would like to learn more about how to use "
                    "pdappend -> https://github.com/cnp0/pdappend/wiki",
                    "",
                    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
                    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
                    "",
                ]
            )
        )

        os.system("pdappend --help")

        return

    logging.debug(f"pdappend setup {str(args)}")

    files = []
    for _ in args.targets.values:
        if isinstance(_, list):
            files += unpack_processed_targets(_)
        else:
            files.append(_)

    files = list(set(files))
    df = pdappend.append(files, config=args.flags)
    pdappend.save_result(df, save_as=args.flags.save_as)
