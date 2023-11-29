from sbpykit.rnd import RandomUtils


def test_makeid():
    assert type(RandomUtils.makeid()) is str
