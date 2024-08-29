from ryz.core import Err
from ryz.traceback import get_as_str, set


def test_create_traceback_depth_0():
    def inner(err: Exception):
        set(err, 0)

    err = Err("hello")
    # use extra function for more informative stack
    inner(err)
    tb_str = get_as_str(err)
    assert tb_str

def test_create_traceback_depth_1():
    def inner(err: Exception):
        set(err, 1)

    err = Exception("hello")
    # use extra function for more informative stack
    inner(err)
    tb_str = get_as_str(err)
    assert tb_str

def test_create_traceback_depth_2():
    def inner(err: Exception):
        set(err, 2)

    err = Exception("hello")
    # use extra function for more informative stack
    inner(err)
    tb_str = get_as_str(err)
    assert tb_str
