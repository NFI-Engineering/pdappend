import os
from pdappend import pdappend, cli, dtypes
from tkinter import filedialog
from tkinter import *


def main():
    root = Tk()
    root.withdraw()
    files = filedialog.askopenfilenames(
        initialdir=os.getcwd(), filetypes=[(".xlsx .xls .csv", ".xlsx .xls .csv")]
    )

    args = dtypes.Args(
        targets=dtypes.Targets(values=files), flags=pdappend.DEFAULT_CONFIG
    )
    cli.main(args)
