from pykit.errors.expect import (
    LengthExpectError,
    NameExpectError,
    TypeExpectError,
)


def test_name():
    error: NameExpectError = NameExpectError(
        "goodbye",
        "hello",
    )

    assert error.args[0] == "goodbye expected to have name hello"


def test_length():
    input_iterable: list[int] = [1, 2, 3]
    error: LengthExpectError = LengthExpectError(
        input_iterable,
        5,
    )

    assertion_message: str = \
        f"iterable {input_iterable} expected to be of" \
        f" length 5, got length 3"

    assert error.args[0] == assertion_message


def test_type():
    error = TypeExpectError(
        obj=10,
        expected=(str, "instance"),
        ActualType=int,
    )
    assertion_message: str = \
        f"object 10 is expected to be instance of type {str}" \
        f": got {int} instead"
    assert error.args[0] == assertion_message


def test_type_class():
    error = TypeExpectError(
        obj=int,
        expected=(str, "subclass"),
        ActualType=int,
    )
    assertion_message: str = \
        f"object {int} is expected to be subclass of type {str}" \
        f": got {int} instead"
    assert error.args[0] == assertion_message


def test_type_multiple():
    error = TypeExpectError(
        obj=10,
        expected=[(str, "instance"), (bool, "strict")],
        ActualType=int,
    )
    assertion_message: str = \
        f"object 10 is expected to be instance of type {str}," \
        f" or to strictly have type {bool}" \
        f": got {int} instead"
    assert error.args[0] == assertion_message
