"""
Check is like an assert, but available in production.

Must never happen => assert
Could happen and must be validated => check

This is a new version of "validation" module.
"""
from typing import Any, NoReturn

from fcode import code

from pykit.types import T


@code("pykit.check-err")
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
        t: type | tuple[type],
    ):
        if not isinstance(obj, t):
            raise CheckErr(f"{obj} must be an instance of {t}")

    @classmethod
    def subclass(
        cls,
        obj: Any,
        t: type | tuple[type],
    ):
        if not issubclass(obj, t):
            raise CheckErr(f"{obj} must be a subclass of {t}")

    @classmethod
    def type(
        cls,
        obj: Any,
        t: type | tuple[type],
    ):
        if type(obj) is not t:
            raise CheckErr(f"{obj} type {type(obj)} must be a {t}")

