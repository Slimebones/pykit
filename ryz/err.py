import re
from typing import Iterator, NoReturn, Self
from pydantic import BaseModel

def panic(msg: str | None = None) -> NoReturn:
    raise Error(msg, Errcode.Panic)

class Errcode:
    Err = "err"
    Panic = "panic"
    ValErr = "val_err"
    NotFoundErr = "not_found_err"
    AlreadyProcessedErr = "already_processed_err"
    UnsupportedErr = "unsupported_err"
    LockErr = "lock_err"

class Error(Exception):
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

    def err(self) -> Error:
        """
        Return the error.
        """
        return self._value

    @property
    def value(self) -> Error:
        """
        Return the inner value.

        @deprecated Use `okval` or `errval` instead. This method will be
        removed in a future version.
        """
        warn(
            "Accessing `.value` on Result type is deprecated, please use "
            + "`.okval` or '.errval' instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._value

    @property
    def errval(self) -> Error:
        """
        Return the inner value.
        """
        return self._value

    def get_err(self) -> Exception:
        errval = self.errval
        if not isinstance(errval, Exception):
            errval = Exception(errval)
        return errval

    def expect(self, message: str) -> NoReturn:
        """
        Raises an `UnwrapErr`.
        """
        exc = UnwrapErr(
            self,
            f"{message}: {self._value!r}",
        )
        if isinstance(self._value, BaseException):
            raise exc from self._value
        raise exc

    def expect_err(self, _message: str) -> Error:
        """
        Return the inner value
        """
        return self._value

    def unwrap(self) -> NoReturn:
        """
        Raises an `UnwrapErr`.
        """
        exc = UnwrapErr(
            self,
            f"Called `Result.unwrap()` on an `Err` value: {self._value!r}",
        )
        if isinstance(self._value, BaseException):
            raise exc from self._value
        raise exc

    def unwrap_err(self) -> Error:
        """
        Return the inner value
        """
        return self._value

    def unwrap_or(self, default: U) -> U:
        """
        Return `default`.
        """
        return default

    def unwrap_or_else(self, op: Callable[[Error], T_co]) -> T_co:
        """
        The contained result is ``Err``, so return the result of applying
        ``op`` to the error value.
        """
        return op(self._value)

    def unwrap_or_raise(self, e: type[TBE]) -> NoReturn:
        """
        The contained result is ``Err``, so raise the exception with the value.
        """
        raise e(self._value)

    def map(self, op: object) -> Err[Error]:
        """
        Return `Err` with the same value
        """
        return self

    async def map_async(self, op: object) -> Err[Error]:
        """
        The contained result is `Ok`, so return the result of `op` with the
        original value passed in
        """
        return self

    def map_or(self, default: U, op: object) -> U:
        """
        Return the default value
        """
        return default

    def map_or_else(self, default_op: Callable[[], U], op: object) -> U:
        """
        Return the result of the default operation
        """
        return default_op()

    def map_err(self, op: Callable[[Error], F]) -> Err[F]:
        """
        The contained result is `Err`, so return `Err` with original error
        mapped to a new value using the passed in function.
        """
        return Err(op(self._value))

    def and_then(self, op: object) -> Err[Error]:
        """
        The contained result is `Err`, so return `Err` with the original value
        """
        return self

    async def and_then_async(self, op: object) -> Err[Error]:
        """
        The contained result is `Err`, so return `Err` with the original value
        """
        return self

    def or_else(
            self, op: Callable[[Error], Result[T_co, F]]) -> Result[T_co, F]:
        """
        The contained result is `Err`, so return the result of `op` with the
        original value passed in
        """
        return op(self._value)

    def inspect(self, op: Callable[[T_co], Any]) -> Result[T_co, Error]:
        """
        Calls a function with the contained value if `Ok`. Returns the original
        result.
        """
        return self

    def inspect_err(self, op: Callable[[Error], Any]) -> Result[T_co, Error]:
        """
        Calls a function with the contained value if `Err`. Returns the
        original result.
        """
        op(self._value)
        return self

    def eject(self) -> NoReturn:
        """
        Same as unwrap, but, instead of UnwrapErr, raises the original err
        value of Res.
        """
        _eject(self)
        # shouldn't get to this point
        raise AssertionError

    def ignore(self):
        """
        Used to signify that the result intentially ignored.

        Useful to avoid linter errors on intentional behaviour.
        """
        _ignore(self)

    def track(self, msg: Any = "tracked", v: int = 1) -> str | None:
        if isinstance(self.errval, Exception):
            return log.track(self.errval, msg, v)
        return None

    async def atrack(self, msg: Any = "tracked", v: int = 1) -> str | None:
        if isinstance(self.errval, Exception):
            return await log.atrack(self.errval, msg, v)
        return None
