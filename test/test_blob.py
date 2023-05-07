from pathlib import Path
import os
import sys

code_dir = Path(__file__).parent.parent.absolute()

sys.path.insert(0,str(code_dir))

from videoapi import __version__
from videoapi.services.blob_storage import BlobStorage


def test_blob_connection():
    assert True
