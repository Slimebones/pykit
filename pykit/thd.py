"""
Transaction handling aka THD.
"""

import inspect
import typing
from typing import Any, Awaitable, Callable, Coroutine, Self

from pykit.err import InpErr, LockErr
from pykit.log import log
from pykit.types import T

_RollbackFnAndPreResult = tuple[
    Callable[[Any], Awaitable[None] | None],
    Any,
]

class Thd:
    # TODO:
    #       maybe add modes:
    #           "standard" => execute right away,
    #           "defer" => execute only on commit
    def __init__(self):
        self._is_queue_locked = False
        self._rollback_stack: list[_RollbackFnAndPreResult] = []

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        err_type,
        err_val: BaseException | None,
        err_traceback,
    ):
        self._is_queue_locked = True
        if err_val:
            while len(self._rollback_stack) != 0:
                fn, preresult = self._rollback_stack.pop()
                if inspect.iscoroutine(fn):
                    raise InpErr(f"expected corofn, but coroutine {fn}")
                try:
                    if inspect.iscoroutinefunction(fn):
                        await fn(preresult)
                        return
                    fn(preresult)
                except Exception as err:
                    log.warn(
                        "catch err (below) during rollback, during execution"
                        f" of fn {fn} => continue",
                    )
                    log.catch(err)

    def a(
        self,
        fn: Callable[[], T],
        rollback_fn: Callable[[T], Any],
    ) -> T:
        if self._is_queue_locked:
            raise LockErr("thd queue")
        f = fn()
        self._rollback_stack.append((rollback_fn, f))
        return f

    def a_delete(
        self,
        fn: Callable[[], T],
    ) -> T:
        return self.a(fn, lambda d: d.delete())

    def a_delete_arr_index(
        self,
        index: int,
        fn: Callable[[], T],
    ) -> T:
        return self.a(
            fn,
            lambda arr: typing.cast(list, arr)[index].delete(),
        )

    async def aa_delete(
        self,
        fn: Coroutine[Any, Any, T],
    ) -> T:
        async def delete(val: T):
            val.delete.delete()

        return await self.aa(fn, delete)

    async def aa(
        self,
        fn: Coroutine[Any, Any, T],
        rollback_corofn: Callable[[T], Awaitable[Any]],
    ) -> T:
        if self._is_queue_locked:
            raise LockErr("thd queue")
        f = await fn
        self._rollback_stack.append((rollback_corofn, f))
        return f

