"""
Core things we use to maintain python programs.
"""
import re
from inspect import isfunction
from typing import (
    Any,
    Callable,
    Coroutine,
    Generic,
    Iterable,
    Literal,
    NoReturn,
    ParamSpec,
    Self,
    TypeAlias,
    TypeVar,
)

from pydantic import BaseModel

from ryz import log
from ryz.core import Err, ecode
from ryz.lock import Lock
from ryz.obj import get_fqname
from ryz.traceback import create_traceback

__all__ = [
    "Ok",
    "Res",
    "Err",
    "ecode",
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

    @property
    def ok(self) -> T_co:
        """
        Return the value.
        """
        return self._value

    @property
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

Res: TypeAlias = Ok[T_co] | Err

class Err(Exception):
    def __init__(
        self, msg: str | None = None, code: str = ecode.Err,
    ) -> None:
        if not re.match(r"^[a-z][0-9a-z]*(_[0-9a-z]+)*$", code):
            panic(f"invalid code {code}")
        self.code = code
        self.msg = msg
        final = code
        if msg:
            final += ": " + msg
        # since we don't raise, for each err we create traceback dynamically
        # upon creation, and we skip 2 frames: `create_traceback` function
        # frame, and this function frame
        create_traceback(self, 2)
        super().__init__(final)

    def __hash__(self) -> int:
        return hash(self.code)

    def is_(self, code: str) -> bool:
        return self.code == code

    @classmethod
    def from_native(cls, exc: Exception) -> Self:
        return cls(";".join(exc.args))

    def is_ok(self) -> Literal[False]:
        return False

    def is_err(self) -> Literal[True]:
        return True

    @property
    def ok(self) -> None:
        """
        Return `None`.
        """
        return

    @property
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

CODE_MAX_LEN: int = 256

T = TypeVar("T")
class Coded(BaseModel, Generic[T]):
    """
    Arbitrary data coupled with identification code.

    Useful when data is type that doesn't support ``code() -> str`` signature.
    """
    code: str
    val: T

class Code:
    """
    Manages attached to various objects str codes.
    """
    _code_to_type: dict[str, type] = {}
    _codes: list[str] = []
    _lock: Lock = Lock()

    @classmethod
    def has_code(cls, code: str) -> bool:
        return code in cls._codes

    @classmethod
    async def get_regd_code_by_id(cls, id: int) -> Res[str]:
        await cls._lock.wait()
        if id > len(cls._codes) - 1:
            return Err(f"codeid {id} is not regd")
        return Ok(cls._codes[id])

    @classmethod
    async def get_regd_codeid_by_type(cls, t: type) -> Res[int]:
        code_res = await cls.get_regd_code_by_type(t)
        if isinstance(code_res, Err):
            return code_res
        code = code_res.ok
        return await cls.get_regd_codeid(code)

    @classmethod
    async def get_regd_codes(cls) -> Res[list[str]]:
        await cls._lock.wait()
        return Ok(cls._codes.copy())

    @classmethod
    async def get_regd_code_by_type(cls, t: type) -> Res[str]:
        await cls._lock.wait()
        for c, t_ in cls._code_to_type.items():
            if t_ is t:
                return Ok(c)
        return Err(f"type {t} is not regd")

    @classmethod
    async def get_regd_codeid(cls, code: str) -> Res[int]:
        await cls._lock.wait()
        if code not in cls._codes:
            return Err(f"code {code} is not regd")
        return Ok(cls._codes.index(code))

    @classmethod
    async def get_regd_type_by_code(cls, code: str) -> Res[type]:
        await cls._lock.wait()
        if code not in cls._code_to_type:
            return Err(f"code {code} is not regd")
        return Ok(cls._code_to_type[code])

    @classmethod
    async def upd(
        cls,
        types: Iterable[type | Coded[type]],
        order: list[str] | None = None,
    ) -> Res[None]:
        async with cls._lock:
            for t in types:
                final_t: type
                if isinstance(t, Coded):
                    code = t.code
                    final_t = t.val
                else:
                    code_res = cls.get_from_type(t)
                    if isinstance(code_res, Err):
                        log.err(
                            f"cannot get code for type {t}: {code_res.err}"
                            " => skip")
                        continue
                    code = code_res.ok
                    final_t = t

                validate_res = cls.validate(code)
                if isinstance(validate_res, Err):
                    log.err(
                        f"code {code} is not valid:"
                        f" {validate_res.err} => skip")
                    continue

                cls._code_to_type[code] = final_t

            cls._codes = list(cls._code_to_type.keys())
            if order:
                order_res = cls._order(order)
                if isinstance(order_res, Err):
                    return order_res

            return Ok(None)

    @classmethod
    def destroy(cls):
        cls._code_to_type.clear()
        cls._codes.clear()
        cls._lock = Lock()

    @classmethod
    def _order(cls, order: list[str]) -> Res[None]:
        sorted_codes: list[str] = []
        for o in order:
            if o not in cls._codes:
                log.warn(f"unrecornized order code {o} => skip")
                continue
            cls._codes.remove(o)
            sorted_codes.append(o)

        # bring rest of the codes
        sorted_codes.extend(cls._codes)

        cls._codes = sorted_codes
        return Ok(None)

    @classmethod
    def validate(cls, code: str) -> Res[None]:
        if not isinstance(code, str):
            return Err(f"code {code} must be str")
        if code == "":
            return Err("empty code")
        for i, c in enumerate(code):
            if i == 0 and not c.isalpha():
                return Err(
                    f"code {code} must start with alpha")
            if not c.isalnum() and c != "_" and c != ":":
                return Err(
                    f"code {code} can contain only alnum"
                    " characters, underscores or semicolons")
        if len(code) > CODE_MAX_LEN:
            return Err(f"code {code} exceeds maxlen {CODE_MAX_LEN}")
        return Ok(None)

    @classmethod
    def get_from_type(cls, t: type) -> Res[str]:
        if isinstance(t, Coded):
            code = t.code
        else:
            codefn = getattr(t, "code", None)
            if codefn is None:
                return Err(
                    f"msg data {t} must define \"code() -> str\" method")
            if not isfunction(codefn):
                return Err(
                    f"msg data {t} \"code\" attribute must be function,"
                    f" got {codefn}")
            try:
                code = codefn()
            except Exception as err:
                log.catch(err)
                return Err(
                    f"err {get_fqname(err)} occured during"
                    f" msg data {t} {codefn} method call #~stacktrace")

        validate_res = cls.validate(code)
        if isinstance(validate_res, Err):
            return validate_res

        return Ok(code)

def resultify(
    fn: Callable[[], T_co],
    errs: tuple[type[Exception], ...] = (Exception,),
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
    errs: tuple[type[Exception], ...] = (Exception,),
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
    raise Err(msg, ecode.Panic)

class ecode:
    Err = "err"
    Panic = "panic_err"
    Val = "val_err"
    NotFound = "not_found_err"
    AlreadyProcessed = "already_processed_err"
    Unsupported = "unsupported_err"
    Lock = "lock_err"
