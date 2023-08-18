from antievil._expect import LengthExpectError, NameExpectError


def test_name():
    error: NameExpectError = NameExpectError(
        ("goodbye", 1),
        "hello",
    )

    assert error.args[0] == "goodbye=<1> expected to have name <hello>"


def test_length():
    input_iterable: list[int] = [1, 2, 3]
    error: LengthExpectError = LengthExpectError(
        input_iterable,
        5,
    )

    assertion_message: str = \
        f"iterable <{input_iterable}> expected to be of" \
        f" length <5>, got length <3>"

    assert error.args[0] == assertion_message
