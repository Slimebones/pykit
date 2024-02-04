"""
Check is like an assert, but available in production.

Must never happen => assert
Could happen and must be validated => check

This is a new version of "validation" module.
"""
from typing import Any
from fcode import code

@code("pykit.check-err")
class CheckErr(Exception):
    def __init__(self, msg: Any):
        super().__init__(msg)

class check:
    @classmethod
    def run(cls, condition: bool, msg: Any = None):
        if not condition:
            raise CheckErr(f"condition failed: {msg}")

    @classmethod
    def instance(
        cls,
        obj: Any,
        t: type | tuple[type]
    ):
        if not isinstance(obj, t):
            raise CheckErr(f"{obj} is not an instance of {t}")

    @classmethod
    def subclass(
        cls,
        obj: Any,
        t: type | tuple[type]
    ):
        if not issubclass(obj, t):
            raise CheckErr(f"{obj} is not a subclass of {t}")

    @classmethod
    def type(
        cls,
        obj: Any,
        t: type | tuple[type]
    ):
        if type(obj) is not t:
            raise CheckErr(f"{obj} type {type(obj)} is not a {t}")

