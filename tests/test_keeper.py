from ryz.keeper import IntKeeper
from ryz.range import Range
from ryz.core import Err


def test_int_keeper():
    k = IntKeeper(Range(0, 5))

    assert k.recv().unwrap() == 0
    assert k.recv().unwrap() == 1
    assert k.recv().unwrap() == 2
    assert k.recv().unwrap() == 3
    assert k.recv().unwrap() == 4
    assert k.recv().unwrap() == 5
    r = k.recv()
    assert isinstance(r, Err)

    k.free(3).unwrap()
    assert k.recv().unwrap() == 3

    r = k.recv()
    assert isinstance(r, Err)
