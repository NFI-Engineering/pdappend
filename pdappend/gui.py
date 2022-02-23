import os

from tkinter import filedialog
from tkinter import Tk

from pdappend import pdappend


def main():
    """Main GUI entrypoint logic. Assumes if there's any configuration it's done
    using .pdappend files."""
    root = Tk()
    root.withdraw()

    filetypes = " ".join(pdappend.FILE_EXTENSIONS_ALLOWED)
    files = filedialog.askopenfilenames(
        initialdir=os.getcwd(),
        # TODO: why does this need (_, _) tuples?
        filetypes=[(filetypes, filetypes)],
    )

    config = pdappend.read_pdappend_file()
    df = pdappend.append(files, config)
    pdappend.save_result(df, config)
