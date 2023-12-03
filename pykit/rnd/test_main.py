from pykit.rnd import RandomUtils


def test_makeid():
    assert isinstance(RandomUtils.makeid(), str)
