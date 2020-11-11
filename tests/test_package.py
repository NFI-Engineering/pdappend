import pandas as pd
import os
from . import test_dir

def test_this_dir():

    # cd to tests/
    os.chdir(test_dir)

    # remove pdappend.csv
    os.system("rm pdappend.csv")

    # run pdappend
    os.system("pdappend")

    rfpath = os.path.join(test_dir, "pdappend.csv")
    
    assert os.path.exists(rfpath)

    df = pd.read_csv(rfpath)

    # TODO: add appended test