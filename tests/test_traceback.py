from ryz.err import ValErr
from ryz.traceback import create_traceback, get_traceback_str


def test_create_traceback_depth_0():
    def inner(err: Exception) -> Exception:
        return create_traceback(err, 0)

    err = ValErr("hello")
    # use extra function for more informative stack
    new_err = inner(err)
    assert err is not new_err, "created side effects"
    tb_str = get_traceback_str(new_err)
    assert tb_str
    assert tb_str.split()[-2] == "tb_lasti=next_frame.f_lasti,"

def test_create_traceback_depth_1():
    def inner(err: Exception) -> Exception:
        return create_traceback(err, 1)

    err = ValErr("hello")
    # use extra function for more informative stack
    new_err = inner(err)
    assert err is not new_err, "created side effects"
    tb_str = get_traceback_str(new_err)
    assert tb_str
    assert tb_str.split()[-3] == "create_traceback(err,"
    assert tb_str.split()[-2] == "1)"

def test_create_traceback_depth_2():
    def inner(err: Exception) -> Exception:
        return create_traceback(err, 2)

    err = ValErr("hello")
    # use extra function for more informative stack
    new_err = inner(err)
    assert err is not new_err, "created side effects"
    tb_str = get_traceback_str(new_err)
    assert tb_str
    # [-1] is "^^^^^^^^^^^^^^^", so we get [-2] for proper assertion
    assert tb_str.split()[-2] == "inner(err)"
