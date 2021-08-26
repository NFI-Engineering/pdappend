# import pytest
from pdappend import cli


# @pytest.mark.skip("vscode launch args mixing with cli.Args")
def test_cli():
    cli.main()
