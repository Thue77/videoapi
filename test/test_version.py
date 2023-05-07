from pathlib import Path
import os
import sys

code_dir = Path(__file__).parent.parent.absolute()

sys.path.insert(0,str(code_dir))

from videoapi import __version__


def test_version():
    assert __version__ == '0.1.0'
