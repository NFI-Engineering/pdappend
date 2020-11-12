from pdappend import cli
from tkinter import filedialog
from tkinter import *


def main():
    root = Tk()
    root.withdraw()

    args = cli.Args(dir=filedialog.askdirectory(), sheet_name=None, header_row=None)
    cli.main(args)
