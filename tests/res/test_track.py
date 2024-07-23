from pathlib import Path

from pykit.err import ValErr
from pykit.log import log
from pykit.res import Err


def test_main():
    tracksid = Err(ValErr("hello")).track()
    assert tracksid
    assert Path(log.err_track_dir, f"{tracksid}.log").exists()

async def test_async():
    tracksid = await Err(ValErr("hello")).atrack()
    assert tracksid
    assert Path(log.err_track_dir, f"{tracksid}.log").exists()
