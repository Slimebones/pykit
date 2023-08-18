import inspect
from enum import Enum
from pathlib import Path
from typing import Any, Iterable, Literal

from antievil.utils import ObjectInfo, never

ExpectedInheritanceLiteral = \
    Literal["strict", "instance", "subclass"]


class ExpectedInheritance(Enum):
    """
    Expected type of inheritance.

    Attributes:
        Strict:
            type(a) is B
        Instance:
            isinstance(a, B)
        Subclass:
            issubclass(A, B)
    """
    Strict = "strict"
    Instance = "instance"
    Subclass = "subclass"


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
        expected_inheritance:
            Which inheritance type is expected between object's type and
            ExpectedType. Can be given as an instance of ExpectedInheritance
            enum or as a plain string. If expected inheritance is Subclass,
            the given object should be Class.
        ActualType(optional):
            Actual type of the object shown in error message. Defaults to None,
            i.e. no actual type will be shown.
    """
    def __init__(
        self,
        *,
        obj: Any,
        ExpectedType: type,
        expected_inheritance: ExpectedInheritance | ExpectedInheritanceLiteral,
        ActualType: type | None = None,
    ) -> None:
        message: str = f"object <{obj}> expected to"

        final_expected_inheritance: ExpectedInheritance
        if isinstance(expected_inheritance, str):
            final_expected_inheritance = ExpectedInheritance(
                expected_inheritance,
            )
        else:
            final_expected_inheritance = expected_inheritance

        match final_expected_inheritance:
            case ExpectedInheritance.Strict:
                self._check_is_regular(obj)
                message += f" strictly have type <{ExpectedType}>"
            case ExpectedInheritance.Instance:
                self._check_is_regular(obj)
                message += f" be instance of type <{ExpectedType}>"
            case ExpectedInheritance.Subclass:
                self._check_is_class(obj)
                message += f" be subclass of type <{ExpectedType}>"
            case _:
                never(final_expected_inheritance)

        if ActualType is not None:
            message += f": got <{ActualType}> instead"

        super().__init__(message)

    def _check_is_class(
        self,
        obj: Any,
    ) -> None:
        if not inspect.isclass(obj):
            raise TypeError

    def _check_is_regular(
        self,
        obj: Any,
    ) -> None:
        if inspect.isclass(obj):
            raise TypeError


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


class NameExpectError(ExpectError):
    """
    Some literal name of an object is expected.
    """
    def __init__(
        self,
        objinfo: ObjectInfo | tuple[str, Any] | str,
        name: str,
    ) -> None:
        super().__init__(
            f"{ObjectInfo(objinfo)} expected to have name <{name}>",
        )


class LengthExpectError(ExpectError):
    """
    Some length of an iterable is expected.

    Args:
        iterable:
            Iterable that violated a length expectation.
        expected_length:
            Length expected.
        actual_length(optional):
            Actual length received. If None, it will be calculated out of the
            given iterable. Defaults to None.
    """
    def __init__(
        self,
        iterable: Iterable[Any],
        expected_length: int,
        actual_length: int | None = None,
    ) -> None:
        if actual_length is None:
            actual_length = len(list(iterable))

        super().__init__(
            f"iterable <{iterable}> expected to be of"
            f" length <{expected_length}>, got length <{actual_length}>",
        )
