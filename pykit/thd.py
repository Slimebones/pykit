"""
Transaction handling aka THD.
"""

from asyncio import Queue
import inspect
from typing import Any, Awaitable, Callable, Coroutine, Self

from pydantic import BaseModel
from pykit.log import log
from pykit.types import T
from pykit.err import InpErr, LockErr

_RollbackFnAndPreResult = tuple[
    Callable[[Any], Awaitable[None] | None],
    Any
]

class Thd:
    # todo:
    #       maybe add modes:
    #           "standard" => execute right away,
    #           "defer" => execute only on commit
    def __init__(self):
        self._is_queue_locked = False
        self._rollback_queue = Queue[_RollbackFnAndPreResult]()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        err_type,
        err_val: Exception | None,
        err_traceback
    ):
        self._is_queue_locked = True
        if err_val:
            while not self._rollback_queue.empty():
                fn, preresult = await self._rollback_queue.get()
                try:
                    if inspect.iscoroutine(fn):
                        raise InpErr(f"expected corofn, but coroutine {fn}")
                    if inspect.iscoroutinefunction(fn):
                        await fn(preresult)
                        return
                    fn(preresult)
                except Exception as err:
                    log.warn(
                        "catch err (below) during rollback, during execution of"
                        f" fn {fn} => continue"
                    )
                    log.catch(err)

    def a(
        self,
        fn: Callable[[], T],
        rollback_fn: Callable[[T], None]
    ) -> Any:
        if self._is_queue_locked:
            raise LockErr("thd queue")
        f = fn()
        self._rollback_queue.put_nowait((rollback_fn, f))
        return f

    async def aa(
        self,
        fn: Coroutine[Any, Any, T],
        rollback_corofn: Callable[[T], Awaitable[None]]
    ) -> Any:
        if self._is_queue_locked:
            raise LockErr("thd queue")
        f = await fn
        await self._rollback_queue.put((rollback_corofn, f))
        return f

