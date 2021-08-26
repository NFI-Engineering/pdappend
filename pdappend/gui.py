import os
from pdappend import pdappend, cli
from tkinter import filedialog
from tkinter import *


def main():
    root = Tk()
    root.withdraw()

    # TODO: from pdappend.pdappend.FILE_TYPES
    files = filedialog.askopenfilenames(
        initialdir=os.getcwd(), filetypes=[(".xlsx .xls .csv", ".xlsx .xls .csv")]
    )

    args = pdappend.Args(
        targets=pdappend.Targets(values=files), flags=pdappend.DEFAULT_CONFIG
    )

    cli.main(args)
