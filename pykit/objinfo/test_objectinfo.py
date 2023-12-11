from pykit.objinfo._info import ObjectInfo


def test_main():
    info: ObjectInfo = ObjectInfo[int](("hello", 2))
    assert str(info) == "hello 2"


def test_only_title():
    info: ObjectInfo = ObjectInfo[int]("hello")
    assert str(info) == "hello"


def test_overflow():
    try:
        ObjectInfo[int](("hello", 1, "whocares"))  # type: ignore
    except ValueError:
        return

    raise AssertionError
