"""
Tools for working with dict-like objects.
"""
from typing import Any

from benedict import benedict
from result import Err, Ok
from pykit.err import NotFoundErr
from pykit.res import Res

dpp = benedict
"""
Dict++ - improved dictionary based on benedict.
"""

def get_recursive(q: dict, key: str) -> Res[Any]:
    for k, v in q.items():
        if key == k:
            return Ok(v)
        if isinstance(v, dict):
            nested_res = get_recursive(v, key)
            if (
                    isinstance(nested_res, Err)
                    and isinstance(nested_res.err_value, NotFoundErr)):
                continue
            return nested_res
    return Err(NotFoundErr(f"val for key {key}"))
