import inspect
from enum import Enum
from pathlib import Path
from typing import Any, Iterable, Literal

from pykit.errors._internals import InternalStringUtils
from pykit.never import never

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
        expected:
            Tuple or tuples (expected to be an any type of it) of expected
            types and chosen type check.
        ActualType(optional):
            Actual type of the object shown in error message. Defaults to None,
            i.e. no actual type will be shown.
    """
    Code = "slimebones.pykit.errors.error.type-expect"
    def __init__(
        self,
        *,
        obj: Any,
        expected:
            tuple[type, ExpectedInheritance | ExpectedInheritanceLiteral]
            | list[
                tuple[type, ExpectedInheritance | ExpectedInheritanceLiteral]
            ],
        ActualType: type | None = None,
    ) -> None:
        message: str = f"object {obj} is expected to"

        parsed_expected_list: list[tuple[type, ExpectedInheritance]] = []

        if isinstance(expected, tuple):
            parsed_expected_list.append(
                (expected[0], self._convert_expected_inheritance(expected[1])),
            )
        else:
            parsed_expected_list = [
                (e[0], self._convert_expected_inheritance(e[1]))
                for e in expected
            ]

        is_first_part: bool = True
        for parsed_expected in parsed_expected_list:
            part_prefix: str = " " if is_first_part else " or "

            if is_first_part:
                is_first_part = False

            message += \
                part_prefix \
                + self._get_message_part(obj, parsed_expected) \
                + ","

        # remove last comma
        message = message[:-1]

        if ActualType is not None:
            message += f": got {ActualType} instead"

        super().__init__(message)

    def _convert_expected_inheritance(
        self, raw: ExpectedInheritance | ExpectedInheritanceLiteral,
    ) -> ExpectedInheritance:
        if isinstance(raw, str):
            return ExpectedInheritance(raw)
        else:
            return raw

    def _get_message_part(
        self, obj: Any, expected: tuple[type, ExpectedInheritance],
    ) -> str:
        match expected[1]:
            case ExpectedInheritance.Strict:
                self._check_is_regular(obj)
                return f"to strictly have type {expected[0]}"
            case ExpectedInheritance.Instance:
                self._check_is_regular(obj)
                return f"be instance of type {expected[0]}"
            case ExpectedInheritance.Subclass:
                self._check_is_class(obj)
                return  f"be subclass of type {expected[0]}"
            case _:
                never(expected[1])
                return None

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
    Code = "slimebones.pykit.errors.error.directory-expect"
    def __init__(
        self,
        *,
        path: Path,
    ) -> None:
        message: str = f"path {path} expected to be directory"
        super().__init__(message)


class FileExpectError(ExpectError):
    """
    When some path is expected to lead to non-directory (plain file).
    """
    Code = "slimebones.pykit.errors.error.file-expect"
    def __init__(
        self,
        *,
        path: Path,
    ) -> None:
        message: str = f"path {path} shouldn't be directory"
        super().__init__(message)


class StrExpectError(ExpectError):
    """
    Some string is expected.
    """
    Code = "slimebones.pykit.errors.error.str-expect"
    def __init__(
        self,
        s: str,
        expected_str: str,
    ) -> None:
        super().__init__(
            f"{s} expected to have name {expected_str}",
        )


class NameExpectError(StrExpectError):
    """
    Some literal name of an object is expected.
    """
    Code = "slimebones.pykit.errors.error.name-expect"


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
    Code = "slimebones.pykit.errors.error.length-expect"
    def __init__(
        self,
        iterable: Iterable[Any],
        expected_length: int,
        actual_length: int | None = None,
    ) -> None:
        if actual_length is None:
            actual_length = len(list(iterable))

        super().__init__(
            f"iterable {iterable} expected to be of"
            f" length {expected_length}, got length {actual_length}",
        )


class OneObjectExpectError(ExpectError):
    """
    When only one object is expected to be found after the search.
    """
    Code = "slimebones.pykit.errors.error.one-object-expect"
    def __init__(
        self,
        *,
        title: str,
        found_count: int,
        options: dict,
    ) -> None:
        message: str = \
            f"only one {title} object is expected, but got" \
            f" count {found_count} instead for options:" \
            f" {InternalStringUtils.stringify(options)}"
        super().__init__(message)
