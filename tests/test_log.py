from pathlib import Path

from ryz import log


def test_track():
    def f():
        raise ValueError("hello")

    try:
        f()
    except ValueError as err:
        tracksid = log.track(err, "tracked")
        assert tracksid
        assert Path(log.err_track_dir, f"{tracksid}.log").exists()

async def test_atrack():
    def f():
        raise ValueError("hello")

    try:
        f()
    except ValueError as err:
        tracksid = await log.atrack(err, "tracked")
        assert tracksid
        assert Path(log.err_track_dir, f"{tracksid}.log").exists()
