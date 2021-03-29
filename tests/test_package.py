import pytest
import pdappend


@pytest.mark.skip("vscode laungh args mixing with cli.Args")
def test_cli():
    pdappend.cli.main()

    pass
