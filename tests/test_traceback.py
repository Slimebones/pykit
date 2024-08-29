from ryz.core import Err
from ryz.traceback import get_as_str, set


def test_create_traceback_depth_0():
    def inner(err: Exception) -> Exception:
        return set(err, 0)

    err = Err("hello")
    # use extra function for more informative stack
    new_err = inner(err)
    assert err is not new_err, "created side effects"
    tb_str = get_as_str(new_err)
    assert tb_str
    assert tb_str.split()[-2] == "tb_lasti=next_frame.f_lasti,"

def test_create_traceback_depth_1():
    def inner(err: Exception) -> Exception:
        return set(err, 1)

    err = Exception("hello")
    # use extra function for more informative stack
    new_err = inner(err)
    assert err is not new_err, "created side effects"
    tb_str = get_as_str(new_err)
    assert tb_str
    assert tb_str.split()[-3] == "create_traceback(err,"
    assert tb_str.split()[-2] == "1)"

def test_create_traceback_depth_2():
    def inner(err: Exception) -> Exception:
        return set(err, 2)

    err = Exception("hello")
    # use extra function for more informative stack
    new_err = inner(err)
    assert err is not new_err, "created side effects"
    tb_str = get_as_str(new_err)
    assert tb_str
    # [-1] is "^^^^^^^^^^^^^^^", so we get [-2] for proper assertion
    assert tb_str.split()[-2] == "inner(err)"
