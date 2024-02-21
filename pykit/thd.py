"""
Transaction handling aka THD.
"""

from asyncio import Queue
import inspect
from typing import Any, Callable, Coroutine, Self

from pydantic import BaseModel
from pykit.log import log
from pykit.err import LockErr

class Thd:
    # todo:
    #       maybe add modes:
    #           "standard" => execute right away,
    #           "defer" => execute only on commit
    def __init__(self):
        self._is_queue_locked = False
        self._rollback_queue = Queue()

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
                fn = await self._rollback_queue.get()
                try:
                    if inspect.iscoroutine(fn):
                        await fn
                        return
                    if inspect.iscoroutinefunction(fn):
                        log.warn(
                            "you should pass either callable or coro,"
                            f" got coroutine function {fn} => execute anyway"
                        )
                        await fn()
                        return
                    fn()
                except Exception as err:
                    log.warn(
                        "catch err during rollback, during execution of"
                        f" fn {fn} => continue"
                    )
                    log.catch(err)

    def a(
        self,
        fn: Callable,
        rollback_fn: Callable
    ) -> Any:
        if self._is_queue_locked:
            raise LockErr("thd queue")
        f = fn()
        self._rollback_queue.put_nowait(rollback_fn)
        return f

    async def aa(
        self,
        fn: Coroutine,
        rollback_fn: Coroutine
    ) -> Any:
        if self._is_queue_locked:
            raise LockErr("thd queue")
        f = await fn
        await self._rollback_queue.put(rollback_fn)
        return f

