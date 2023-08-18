from pathlib import Path
from typing import Any


class ExpectError(Exception):
    """
    Some value is expected given some object.

    @abstract
    """


class TypeExpectError(ExpectError):
    """
    Some object should have type or by instance of expected type.

    Args:
        obj:
            Object that failed the expectation.
        ExpectedType:
            The type of object (or parent type) is expected.
        is_instance_expected:
            Whether the object was expected to be an instance of the type, or
            to have a strict expected type (isinstance() vs. type()).
        ActualType(optional):
            Actual type of the object shown in error message. Defaults to None,
            i.e. no actual type will be shown.
    """
    def __init__(
        self,
        *,
        obj: Any,
        ExpectedType: type,
        is_instance_expected: bool,
        ActualType: type | None = None,
    ) -> None:
        message: str = f"object <{obj}> expected to"

        if is_instance_expected:
            message += f" be instance of type <{ExpectedType}>"
        else:
            message += f" strictly have type <{ExpectedType}>"

        if ActualType is not None:
            message += f": got <{ActualType}> instead"

        super().__init__(message)


class DirectoryExpectError(ExpectError):
    """
    When some path is expected to lead to directory.
    """
    def __init__(
        self,
        *,
        path: Path,
    ) -> None:
        message: str = f"path <{path}> expected to be directory"
        super().__init__(message)


class FileExpectError(ExpectError):
    """
    When some path is expected to lead to non-directory (plain file).
    """
    def __init__(
        self,
        *,
        path: Path,
    ) -> None:
        message: str = f"path <{path}> shouldn't be directory"
        super().__init__(message)
