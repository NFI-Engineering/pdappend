import os
import click

from typing import Tuple, List, Set, Union

from pdappend import pdappend, constants, __version__


# https://stackoverflow.com/a/52069546
class DefaultCommandGroup(click.Group):
    """allow a default command for a group"""

    def command(self, *args, **kwargs):
        default_command = kwargs.pop("default_command", False)

        if default_command and not args:
            kwargs["name"] = kwargs.get("name", "<>")

        decorator = super(DefaultCommandGroup, self).command(*args, **kwargs)

        if default_command:

            def new_decorator(f):
                cmd = decorator(f)
                self.default_command = cmd.name
                return cmd

            return new_decorator

        return decorator

    def resolve_command(self, ctx, args):
        try:
            # test if the command parses
            return super(DefaultCommandGroup, self).resolve_command(ctx, args)
        except click.UsageError:
            # command did not parse, assume it is the default command
            args.insert(0, self.default_command)
            return super(DefaultCommandGroup, self).resolve_command(ctx, args)


@click.group(cls=DefaultCommandGroup, invoke_without_command=True)
@click.pass_context
def main(ctx) -> None:
    """Invoked entrypoint to pdappend."""
    if not ctx.invoked_subcommand:
        click.echo(
            "\n".join(
                [
                    "",
                    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
                    "~~~~~~~~~~~~~~ pdappend cli ~~~~~~~~~~~~~~~",
                    "",
                    "Use pdappend to append csv, xlsx, and xls files.",
                    "Wiki: https://github.com/cnpryer/pdappend/wiki.",
                    "",
                    f"Version: pdappend-{__version__}",
                    "",
                    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
                    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
                    "",
                ]
            )
        )

        os.system("pdappend --help")


@main.command()
def version() -> None:
    """Command to print version of package."""
    click.echo(f"pdappend-{__version__}")


@main.command()
def setup() -> None:
    """Create .pdappend file in current working directory."""
    config_string = pdappend.Config().as_config_file()
    filepath = os.path.join(os.getcwd(), ".pdappend")

    with open(filepath, "w") as f:
        f.write(config_string)

    click.echo(f".pdappend file saved to {os.path.dirname(filepath)}")


def filter_files(files: Union[List[str], Tuple[str]]) -> List[str]:
    """Filter internally conflicting files out of a list of files/filepaths."""
    files = list(
        filter(
            lambda x: os.path.basename(x)
            not in pdappend.RESULT_FILENAMES_ALLOWED,
            files,
        )
    )

    return files


def load_files(
    dirpath: str = os.getcwd(),
    recursive: bool = constants.DEFAULT_RECURSIVE,
    ignored_dirs: Union[List[str], Tuple[str]] = [],
) -> List[str]:
    """Load files found in target directory.

    Args:
        dirpath (str, optional): Path to directory. Defaults to os.getcwd().
        recursive (bool, optional): If True, recursively search directory tree.
        ignored_dirs (Union[List[str], Tuple[str]], optional): Directories to
        ignore during searches.

    Returns:
        List[str]: Filepaths found in directory.
    """
    files_loaded = []

    if not recursive:
        for _ in filter_files(files=os.listdir(dirpath)):
            files_loaded.append(os.path.join(dirpath, _))

        return files_loaded

    for path, subdirs, files in os.walk(dirpath, topdown=True):
        subdirs[:] = list(filter(lambda x: x not in ignored_dirs, subdirs))
        files[:] = filter_files(files)
        for name in files:
            files_loaded.append(os.path.join(path, name))

    return files_loaded


def find_target_files(
    arg: click.Argument, files: Union[List[str], Tuple[str]]
) -> Set[str]:
    """Parse filepaths using arg (true target) from files. This could be
    specific filenames or regex wildcard identification strings.

    Args:
        arg (click.Argument): Targetting argument from CLI.
        files (Union[List[str], Tuple[str]]): Files (filepaths or names) to
        match in.

    Returns:
        Set[str]: Found files.
    """
    if arg == ".":
        return [
            _
            for _ in files
            if pdappend.parse_filename_extension(filename=_)
            in pdappend.FILE_EXTENSIONS_ALLOWED
        ]

    found = set()
    for _ in filter(
        lambda x: x.endswith(arg[1:] if arg.startswith("*") else arg), files
    ):
        found.add(_)

    return found


@main.command(default_command=True)
@click.option(
    "--csv-header-row",
    default=constants.DEFAULT_CSV_HEADER_ROW,
    help=constants.CSV_HEADER_ROW_DESCRIPTION,
)
@click.option(
    "--excel-header-row",
    default=constants.DEFAULT_EXCEL_HEADER_ROW,
    help=constants.EXCEL_HEADER_ROW_DESCRIPTION,
)
@click.option(
    "--save-as",
    default=constants.DEFAULT_SAVE_AS,
    help=constants.SAVE_AS_DESCRIPTION,
)
@click.option(
    "--sheet-name",
    default=constants.DEFAULT_SHEET_NAME,
    help=constants.SHEET_NAME_DESCRIPTION,
)
@click.option(
    "--verbose",
    is_flag=True,
    help=constants.VERBOSE_DESCRIPTION,
)
@click.option(
    "--recursive",
    is_flag=True,
    help=constants.RECURSIVE_DESCRIPTION,
)
@click.option(
    "--ignore",
    default=[],
    multiple=True,
    help=constants.RECURSIVE_DESCRIPTION,
)
@click.argument("args", nargs=-1)
def append(args: Tuple[click.Argument], **kwargs) -> None:
    """Command to append targets into one file.

    Example:
        ```
        pdappend [target(s)] [...options]
        ```
        Where `[target(s)]` can be regex to parse cwd using or a list of
        filenames.

    Args:
        args (Tuple[click.Argument]): Arguments passed to `pdappend` that
        aren't subcommands.
    """
    if os.path.exists("pdappend.csv"):
        # https://github.com/cnpryer/pdappend/issues/23
        raise Exception("Remove pdappend.csv from directory.")

    if os.path.exists(".pdappend"):
        click.echo(
            "WARNING: .pdappend file found. "
            "Remove .pdappend if you'd like to use CLI-based configuration."
        )
        config = pdappend.read_pdappend_file()

    else:
        config = pdappend.Config(
            sheet_name=kwargs["sheet_name"],
            csv_header_row=kwargs["csv_header_row"],
            excel_header_row=kwargs["excel_header_row"],
            save_as=kwargs["save_as"],
            verbose=kwargs["verbose"],
            recursive=kwargs["recursive"],
            ignore=kwargs["ignore"],
        )

    all_files = load_files(
        recursive=config.recursive, ignored_dirs=config.ignore
    )
    files = set()
    for arg in args:
        found = find_target_files(arg, files=all_files)
        for _ in found:
            files.add(_)

    files = list(files)
    if not files:
        click.echo(f"Unable to find files from target args: {args}")

        return

    click.echo(f"Appending: {list(map(lambda x: os.path.basename(x), files))}")
    df = pdappend.append(files, config)
    pdappend.save_result(df, config)
