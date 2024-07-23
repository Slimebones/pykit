from pathlib import Path

from pykit.err import ValErr
from pykit.log import log
from pykit.res import Err


def test_main():
    tracksid = Err(ValErr("hello")).track()
    assert tracksid
    path = Path(log.err_track_dir, f"{tracksid}.log")
    assert path.exists()
    last_part = path.open("r").read().split()[-1]
    assert \
            last_part \
            == "Err(ValErr(\"hello\")).track()", \
        last_part

async def test_async():
    tracksid = await Err(ValErr("hello")).atrack()
    assert tracksid
    path = Path(log.err_track_dir, f"{tracksid}.log")
    assert path.exists()
    last_part = path.open("r").read().split()[-1]
    assert \
            last_part \
            == "Err(ValErr(\"hello\")).atrack()", \
        last_part
