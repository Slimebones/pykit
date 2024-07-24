from pathlib import Path
import traceback

from pykit.res import Err


def test_tb():
    """
    Res::Err must collect traceback of an Exception upon creation.
    """
    err = Err(Exception("hello"))

    assert Path(
            traceback.extract_tb(err.errval.__traceback__)[-1].filename
        ).name == "test_err.py"
