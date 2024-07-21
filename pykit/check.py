"""
Check is like an assert, but available in production.

Must never happen => assert
Could happen and must be validated => check

This is a new version of "validation" module.
"""
from typing import Any, Callable, Coroutine, Iterable, NoReturn

from pykit.res import Err
from pykit.types import T, TIterable


class CheckErr(Exception):
    pass

class check:
    @classmethod
    def fail(cls, msg: Any = None) -> NoReturn:
        msgf = ": " + msg if msg else ""
        raise CheckErr(f"statement shouldn't be reached{msgf}")

    @classmethod
    def run(cls, condition: bool, msg: Any = None):
        msgf = ": " + msg if msg else ""
        if not condition:
            raise CheckErr(f"condition failed{msgf}")

    @classmethod
    def evaltrue(cls, obj: T | None) -> T:
        if not obj:
            raise CheckErr("condition failed: obj must eval to true")
        return obj

    @classmethod
    def notnone(cls, obj: T | None) -> T:
        if obj is None:
            raise CheckErr("condition failed: obj must not be None")
        return obj

    @classmethod
    def instance(
        cls,
        obj: Any,
        t: type[T] | tuple[type[T]],
    ) -> T:
        if not isinstance(obj, t):
            raise CheckErr(f"{obj} must be an instance of {t}")
        return obj

    @classmethod
    def subclass(
        cls,
        obj: Any,
        t: type[T] | tuple[type[T]],
    ) -> type[T]:
        if not issubclass(obj, t):
            raise CheckErr(f"{obj} must be a subclass of {t}")
        return obj

    @classmethod
    def each_type(
        cls,
        objs: Iterable[Any],
        t: type[T] | tuple[type[T]],
    ) -> Iterable[T]:
        for o in objs:
            check.type(o, t)
        return objs

    @classmethod
    def each_instance(
        cls,
        objs: Iterable[Any],
        t: type[T] | tuple[type[T]],
    ) -> Iterable[T]:
        for o in objs:
            check.instance(o, t)
        return objs

    @classmethod
    def each_subclass(
        cls,
        objs: Iterable[Any],
        t: type[T] | tuple[type[T]],
    ) -> Iterable[T]:
        for o in objs:
            check.subclass(o, t)
        return objs

    @classmethod
    def each_notnone(
        cls,
        objs: TIterable,
    ) -> TIterable:
        for o in objs:
            check.notnone(o)
        return objs

    @classmethod
    def each_evaltrue(
        cls,
        objs: TIterable,
    ) -> TIterable:
        for o in objs:
            check.evaltrue(o)
        return objs

    @classmethod
    def expect(
        cls,
        func: Callable,
        errcls: type[Exception],
        *args,
        **kwargs,
    ) -> None:
        """
        Expects given function to raise given error if function is called with
        given args and kwargs.

        Automatically retrieves result.Err.errval if the func returns it.

        Args:
            fn:
                Function to call.
            errcls:
                Exception class to expect.
            args:
                Positional arguments to pass to function call.
            kwargs:
                Keyword arguments to pass to function call.

        Raises:
            CheckErr:
                Given error has not been raised on function's call.
        """
        try:
            res = func(*args, **kwargs)
        except errcls:
            return
        else:
            if isinstance(res, Err) and isinstance(res.errval, errcls):
                return
            raise CheckErr(
                f"error {errcls} expected on call of function {func}",
            )

    @classmethod
    async def aexpect(
        cls,
        coro: Coroutine,
        errcls: type[Exception],
    ) -> None:
        try:
            await coro
        except errcls:
            pass
        else:
            raise CheckErr(
                f"error {errcls} expected on call of coro {coro}",
            )

    @classmethod
    def type(
        cls,
        obj: Any,
        t: type[T] | tuple[type[T]],
    ) -> T:
        if type(obj) is not t:
            raise CheckErr(f"{obj} type {type(obj)} must be a {t}")
        return obj

