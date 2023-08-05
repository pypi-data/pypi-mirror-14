import sys
import shutil
from backports import shutil_which

which = shutil_which.which

def test_unnecessary_shim():
    if hasattr(shutil, 'which'):
        assert shutil_which.which is shutil.which
    else:
        assert shutil_which.which is shutil_which.backport_which

def test_smoke():
    assert which("nosuchthingasthis") is None
    assert which("sleep") is not None
