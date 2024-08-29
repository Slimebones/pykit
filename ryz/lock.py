import asyncio

from ryz.uuid import uuid4


class Lock:
    def __init__(self) -> None:
        self._evt = asyncio.Event()
        self._evt.set()
        self._owner_token: str | None = None

    async def __aenter__(self):
        await self.acquire()

    async def __aexit__(self, *args):
        assert self._owner_token is not None
        await self.release(self._owner_token)

    def is_locked(self) -> bool:
        return not self._evt.is_set()

    async def acquire(self) -> str:
        await self._evt.wait()
        self._evt.clear()
        self._owner_token = uuid4()
        return self._owner_token

    async def release(self, token: str):
        if self._owner_token is not None and token != self._owner_token:
            raise ValueError("invalid token to unlock")
        self._evt.set()
        self._owner_token = None

    async def wait(self):
        return await self._evt.wait()
