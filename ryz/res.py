"""
Rust-like result for python.

Origins (MIT): https://github.com/rustedpy/result

We primarily use ``Res`` object, but also maintain ``Result`` to conform with
Rust. ``Res`` is more convenient due to collecting of Exception extended data.
"""
from __future__ import annotations

import functools
import inspect
from typing import (
    Any,
    AsyncGenerator,
    Awaitable,
    Callable,
    Coroutine,
    Final,
    Generator,
    Generic,
    Iterator,
    Literal,
    NoReturn,
    ParamSpec,
    Self,
    TypeAlias,
    TypeGuard,
    TypeVar,
    Union,
)
from warnings import warn

from ryz import log
from ryz.err import Errcode, Error
from ryz.traceback import create_traceback

__all__ = [
    "Ok",
    "Res",
    "resultify",
    "aresultify",
    "secure",
    "asecure",
]


T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)  # Success type
U = TypeVar("U")
F = TypeVar("F")
P = ParamSpec("P")
R = TypeVar("R")
TBE = TypeVar("TBE", bound=BaseException)


class Ok(Generic[T_co]):
    """
    A value that indicates success and which stores arbitrary data for the
    return value.
    """

    __match_args__ = ("okval",)
    __slots__ = ("_value",)

    def __iter__(self) -> Iterator[T_co]:
        yield self._value

    def __init__(self, value: T_co = None) -> None:
        self._value = value

    def __repr__(self) -> str:
        return f"Ok({self._value!r})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Ok) and self._value == other._value

    def __ne__(self, other: object) -> bool:
        return not (self == other)

    def __hash__(self) -> int:
        return hash((True, self._value))

    def is_ok(self) -> Literal[True]:
        return True

    def is_err(self) -> Literal[False]:
        return False

    def ok(self) -> T_co:
        """
        Return the value.
        """
        return self._value

    def err(self) -> None:
        """
        Return `None`.
        """
        return

    @property
    def value(self) -> T_co:
        """
        Return the inner value.

        @deprecated Use `okval` or `errval` instead. This method will be
        removed in a future version.
        """
        warn(
            "Accessing `.value` on Result type is deprecated, please use "
            + "`.okval` or `.errval` instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._value

    @property
    def okval(self) -> T_co:
        """
        Return the inner value.
        """
        return self._value

    def expect(self, _message: str) -> T_co:
        """
        Return the value.
        """
        return self._value

    def expect_err(self, message: str) -> NoReturn:
        """
        Raise an UnwrapErr since this type is `Ok`
        """
        raise UnwrapErr(self, message)

    def unwrap(self) -> T_co:
        """
        Return the value.
        """
        return self._value

    def unwrap_err(self) -> NoReturn:
        """
        Raise an UnwrapErr since this type is `Ok`
        """
        raise UnwrapErr(self, "Called `Result.unwrap_err()` on an `Ok` value")

    def unwrap_or(self, _default: object) -> T_co:
        """
        Return the value.
        """
        return self._value

    def unwrap_or_else(self, op: object) -> T_co:
        """
        Return the value.
        """
        return self._value

    def unwrap_or_raise(self, e: object) -> T_co:
        """
        Return the value.
        """
        return self._value

    def map(self, op: Callable[[T_co], U]) -> Ok[U]:
        """
        The contained result is `Ok`, so return `Ok` with original value mapped
        to a new value using the passed in function.
        """
        return Ok(op(self._value))

    async def map_async(
        self, op: Callable[[T_co], Awaitable[U]],
    ) -> Ok[U]:
        """
        The contained result is `Ok`, so return the result of `op` with the
        original value passed in
        """
        return Ok(await op(self._value))

    def map_or(self, default: object, op: Callable[[T_co], U]) -> U:
        """
        The contained result is `Ok`, so return the original value mapped to a
        new value using the passed in function.
        """
        return op(self._value)

    def map_or_else(self, default_op: object, op: Callable[[T_co], U]) -> U:
        """
        The contained result is `Ok`, so return original value mapped to
        a new value using the passed in `op` function.
        """
        return op(self._value)

    def map_err(self, op: object) -> Ok[T_co]:
        """
        The contained result is `Ok`, so return `Ok` with the original value
        """
        return self

    def and_then(
        self, op: Callable[[T_co], Result[U, Error]]
    ) -> Result[U, Error]:
        """
        The contained result is `Ok`, so return the result of `op` with the
        original value passed in
        """
        return op(self._value)

    async def and_then_async(
        self, op: Callable[[T_co], Awaitable[Res[U]]],
    ) -> Result[U, Error]:
        """
        The contained result is `Ok`, so return the result of `op` with the
        original value passed in
        """
        return await op(self._value)

    def or_else(self, op: object) -> Ok[T_co]:
        """
        The contained result is `Ok`, so return `Ok` with the original value
        """
        return self

    def inspect(self, op: Callable[[T_co], Any]) -> Res[T_co]:
        """
        Calls a function with the contained value if `Ok`. Returns the original
        result.
        """
        op(self._value)
        return self

    def inspect_err(self, op: Callable[[Error], Any]) -> Res[T_co]:
        """
        Calls a function with the contained value if `Err`. Returns the
        original result.
        """
        return self

    def ignore(self):
        """
        Used to signify that the result intentially ignored.

        Useful to avoid linter errors on intentional behaviour.
        """
        _ignore(self)

    def track(self, msg: Any = "tracked"):
        return

    async def atrack(self, msg: Any = "tracked"):
        return

Res = Ok[T_co] | Error

def resultify(
    fn: Callable[[], T_co],
    errs: tuple[type[Exception], ...] = (Exception,)
) -> Res[T_co]:
    """
    Calls a func and wraps retval to Res - to Err on thrown exception, Ok
    otherwise.

    Useful to integrate non-result functions.
    """
    try:
        res = fn()
    except errs as err:
        return Error.from_native(err)
    return Ok(res)

async def aresultify(
    coro: Coroutine[Any, Any, T_co],
    errs: tuple[type[Exception], ...] = (Exception,)
) -> Res[T_co]:
    """
    Calls a func and wraps retval to Res - to Err on thrown exception, Ok
    otherwise.

    Useful to integrate non-result functions.
    """
    try:
        res = await coro
    except errs as err:
        return Error.from_native(err)
    return Ok(res)

def _ignore(res: Res):
    """
    Used to signify that the result intentially ignored.

    Useful to avoid linter errors on intentional behaviour.
    """

def secure(fn: Callable[[], Res[T_co]]) -> Res[T_co]:
    """
    Wraps function raised error into Err(e), or returns as it is.
    """
    try:
        return fn()
    except Exception as err:
        return Error.from_native(err)

async def asecure(coro: Coroutine[Any, Any, Res[T_co]]) -> Res[T_co]:
    """
    Wraps function raised error into Err(e), or returns as it is.
    """
    try:
        return await coro
    except Exception as err:
        return Error.from_native(err)
