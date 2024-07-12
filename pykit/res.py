from typing import Callable, TypeVar

from result import Err, Ok, Result

__all__ = [
    "Ok",
    "Err",
    "Result"
]

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)
Res = Result[T_co, Exception]
"""
Short version of result.Result, where err value is always an Exception.
"""

def raise_err_val(func: Callable):
    """
    Calls a func and raises Err.err_value if func returns it.
    """
    res = func()
    if isinstance(res, Err):
        raise res.err_value

def try_or_res(
        func: Callable[[], T_co],
        errs: tuple[type[Exception], ...] = (Exception,)) -> Res[T_co]:
    """
    Calls a func and wraps raised exception, otherwise return func retval.
    """
    try:
        res = func()
    except errs as err:
        return Err(err)
    return Ok(res)

T = TypeVar("T")
def eject(res: Res[T]) -> T:
    """
    Same as unwrap, but, instead of UnwrapError, raises the original err value
    of Res.
    """
    if isinstance(res, Err):
        raise res.err_value
    return res.ok_value
