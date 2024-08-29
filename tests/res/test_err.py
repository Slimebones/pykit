import traceback
from pathlib import Path

from ryz.core import Err


def test_tb():
    """
    res::Err must collect traceback of an Exception upon creation.
    """
    err = Err(Exception("hello"))
    assert err.errval.__traceback__ is not None

    stack_summary = traceback.extract_tb(err.errval.__traceback__)
    assert Path(stack_summary[-1].filename).name == "test_err.py"
