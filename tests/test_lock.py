from pykit.lock import Lock

async def test_with():
    lock = Lock()
    async with lock:
        assert lock.is_locked
    assert not lock.is_locked
