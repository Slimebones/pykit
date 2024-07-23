from pathlib import Path

from pykit.res import Err


def test_tb():
    """
    Res::Err must collect traceback of an Exception upon creation.
    """
    err = Err(Exception("hello"))
    assert Path(err.stack_summary[-1].filename).name == "test_err.py"
