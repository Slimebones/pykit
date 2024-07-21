from pykit.check import check
from pykit.err import ValErr
from pykit.res import Err, Ok


def test_eject():
    res = Ok(1)
    res.eject()

    res = Err(ValErr("hello"))
    check.expect(res.eject, ValErr)
