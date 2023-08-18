from antievil._expect import NameExpectError


def test_name():
    error: NameExpectError = NameExpectError(
        ("goodbye", 1),
        "hello",
    )

    assert error.args[0] == "goodbye=<1> expected to have name <hello>"
