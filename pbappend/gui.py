import os
from tkinter import Tk, filedialog

from pbappend import pbappend


def main():
    """Main GUI entrypoint logic. Assumes if there's any configuration it's done
    using .pbappend files."""
    root = Tk()
    root.withdraw()

    filetypes = " ".join(pbappend.FILE_EXTENSIONS_ALLOWED)
    files = filedialog.askopenfilenames(
        initialdir=os.getcwd(),
        # TODO: why does this need (_, _) tuples?
        filetypes=[(filetypes, filetypes)],
    )

    config = pbappend.read_pbappend_file()
    df = pbappend.append(files, config)
    pbappend.save_result(df, config)
