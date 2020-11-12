from pdappend.cli import main as cli  # TODO: improve this
from tkinter import filedialog
from tkinter import *
from collections import namedtuple

Args = namedtuple("args", ["dir"])


def main():
    root = Tk()
    root.withdraw()

    args = Args(dir=filedialog.askdirectory())
    cli(args)
