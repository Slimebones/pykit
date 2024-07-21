"""
Tools for working with dict-like objects.
"""
from typing import TypeVar

from pykit.err import NotFoundErr
from pykit.res import Err, Ok, Res

T = TypeVar("T")

def get_recursive(d: dict, key: str, default: T | None = None) -> Res[T]:
    for k, v in d.items():
        if key == k:
            return Ok(v)
        if isinstance(v, dict):
            nested_res = get_recursive(v, key)
            if (
                    isinstance(nested_res, Err)
                    and isinstance(nested_res.errval, NotFoundErr)):
                continue
            return nested_res
    if default is None:
        return Err(NotFoundErr(f"val for key {key}"))
    return Ok(default)
