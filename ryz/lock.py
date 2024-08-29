import asyncio

from ryz.core import Err, Ok, Res
from ryz.uuid import uuid4


class Lock:
    def __init__(self) -> None:
        self._evt = asyncio.Event()
        self._evt.set()
        self._owner_token: str | None = None

    async def __aenter__(self):
        (await self.acquire()).unwrap()

    async def __aexit__(self, *args):
        assert self._owner_token is not None
        (await self.release(self._owner_token)).unwrap()

    def is_locked(self) -> bool:
        return not self._evt.is_set()

    async def acquire(self) -> Res[str]:
        await self._evt.wait()
        self._evt.clear()
        self._owner_token = uuid4()
        return Ok(self._owner_token)

    async def release(self, token: str) -> Res[None]:
        if self._owner_token is not None and token != self._owner_token:
            return Err("invalid token to unlock")
        self._evt.set()
        self._owner_token = None
        return Ok(None)

    async def wait(self):
        return await self._evt.wait()
