"""
Tools for working with dict-like objects.
"""
from typing import TypeVar

from ryz.core import Err, Ok, Res, ecode

T = TypeVar("T")

def get_recursive(d: dict, key: str, default: T | None = None) -> Res[T]:
    for k, v in d.items():
        if key == k:
            return Ok(v)
        if isinstance(v, dict):
            nested_res = get_recursive(v, key)
            if (
                isinstance(nested_res, Err)
                and nested_res.err.code == ecode.NotFound
            ):
                continue
            return nested_res
    if default is None:
        return Err(f"val for key {key}", ecode.NotFound)
    return Ok(default)
