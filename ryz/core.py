"""
Core things we use to maintain python programs.
"""
import re
from typing import Any, Callable, Iterator, Literal, NoReturn, ParamSpec, Self, TypeVar
from pydantic import BaseModel
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
from ryz.core import Errcode, Err
from ryz.traceback import create_traceback

__all__ = [
    "Ok",
    "Res",
    "Err",
    "Errcode",
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

    def expect(self, _message: str) -> T_co:
        """
        Return the value.
        """
        return self._value

    def unwrap(self) -> T_co:
        """
        Return the value.
        """
        return self._value

    def inspect(self, fn: Callable[[T_co], Any]) -> "Res[T_co]":
        """
        Calls a function with the contained value if `Ok`. Returns the original
        result.
        """
        fn(self._value)
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

Res = Ok[T_co] | Err

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
        return Err.from_native(err)
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
        return Err.from_native(err)
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
        return Err.from_native(err)

async def asecure(coro: Coroutine[Any, Any, Res[T_co]]) -> Res[T_co]:
    """
    Wraps function raised error into Err(e), or returns as it is.
    """
    try:
        return await coro
    except Exception as err:
        return Err.from_native(err)

def panic(msg: str | None = None) -> NoReturn:
    raise Err(msg, Errcode.Panic)

class Errcode:
    Err = "err"
    Panic = "panic"
    ValErr = "val_err"
    NotFoundErr = "not_found_err"
    AlreadyProcessedErr = "already_processed_err"
    UnsupportedErr = "unsupported_err"
    LockErr = "lock_err"

class Err(Exception):
    def __init__(
        self, msg: str | None = None, code: str = Errcode.Err
    ) -> None:
        if not re.match(r"^[a-z][0-9a-z]*(_[0-9a-z]+)*$", code):
            panic(f"invalid code {code}")
        self.code = code
        self.msg = msg
        final = code
        if msg:
            final += ": " + msg
        super().__init__(final)

    def __iter__(self) -> Iterator[NoReturn]:
        def _iter() -> Iterator[NoReturn]:
            # Exception will be raised when the iterator is advanced, not when
            # it's created
            raise Exception(self)
            # This yield will never be reached, but is necessary to create a
            # generator
            yield

        return _iter()

    def __hash__(self) -> int:
        return hash(self.code)

    @classmethod
    def from_native(cls, exc: Exception) -> Self:
        return cls(";".join(exc.args))

    def is_ok(self) -> Literal[False]:
        return False

    def is_err(self) -> Literal[True]:
        return True

    def ok(self) -> None:
        """
        Return `None`.
        """
        return

    def err(self) -> Self:
        """
        Return the error.
        """
        return self

    def unwrap(self) -> NoReturn:
        """
        Raises an `UnwrapErr`.
        """
        raise self

    def inspect(self, fn: Callable[[T_co], Any]) -> Res[T_co]:
        """
        Calls a function with the contained value if `Ok`. Returns the original
        result.
        """
        return self

    def ignore(self):
        """
        Used to signify that the result intentially ignored.

        Useful to avoid linter errors on intentional behaviour.
        """
        _ignore(self)

    def track(self, msg: Any = "tracked", v: int = 1) -> str | None:
        if isinstance(self, Exception):
            return log.track(self, msg, v)
        return None

    async def atrack(self, msg: Any = "tracked", v: int = 1) -> str | None:
        if isinstance(self, Exception):
            return await log.atrack(self, msg, v)
        return None
