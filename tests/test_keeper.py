from pykit.check import check
from pykit.err import ValueErr
from pykit.keeper import IntKeeper
from pykit.range import Range


def test_int_keeper():
    k = IntKeeper(Range(0, 5))

    assert k.recv().unwrap() == 0
    assert k.recv().unwrap() == 1
    assert k.recv().unwrap() == 2
    assert k.recv().unwrap() == 3
    assert k.recv().unwrap() == 4
    assert k.recv().unwrap() == 5
    check.expect(k.recv, ValueErr)

    k.free(3).unwrap()
    assert k.recv().unwrap() == 3
    check.expect(k.recv, ValueErr)
