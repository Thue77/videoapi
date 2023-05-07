from pathlib import Path
import os
import sys

code_dir = Path(__file__).parent.parent.absolute()

sys.path.insert(0,str(code_dir))

import videoapi.services.secret_scope as secret_scope



def test_secret_is_redacted():
    assert "REDACTED" == str(secret_scope.Secret('Some secret value'))