from typing import Callable, Iterable, TypeVar

from result import Result, Err

T_co = TypeVar("T_co", covariant=True)
Res = Result[T_co, Exception]
"""
Short version of result.Result, where err value is always an Exception.
"""

def raise_err_value(func: Callable):
    """
    Calls a func and raises Err.err_value if func returns it.
    """
    res = func()
    if isinstance(res, Err):
        raise res.err_value

def try_or_res(func: Callable, errs: tuple[type[Exception], ...] = (Exception,)):
    """
    Calls a func and wraps any raised exception
    """
    try:
        func()
    except errs as err:
        return
