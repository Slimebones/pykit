from typing import TypeVar

from result import Result

T_co = TypeVar("T_co", covariant=True)
Res = Result[T_co, Exception]
"""
Short version of result.Result, where err value is always an Exception.
"""
