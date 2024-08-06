from pathlib import Path

from ryz.err import ValErr
from ryz.log import log


def test_track():
    def f():
        raise ValErr("hello")

    try:
        f()
    except ValErr as err:
        tracksid = log.track(err, "tracked")
        assert tracksid
        assert Path(log.err_track_dir, f"{tracksid}.log").exists()

async def test_atrack():
    def f():
        raise ValErr("hello")

    try:
        f()
    except ValErr as err:
        tracksid = await log.atrack(err, "tracked")
        assert tracksid
        assert Path(log.err_track_dir, f"{tracksid}.log").exists()
