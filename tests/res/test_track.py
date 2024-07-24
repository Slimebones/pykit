from pathlib import Path

from pykit.err import ValErr
from pykit.log import log
from pykit.res import Err


def test_main():
    tracksid = Err(ValErr("hello")).track()
    assert tracksid
    path = Path(log.err_track_dir, f"{tracksid}.log")
    assert path.exists()
    target_part = path.open("r").read().split()[-4]
    assert \
            target_part \
            == "Err(ValErr(\"hello\")).track()", \
        target_part

async def test_async():
    tracksid = await Err(ValErr("hello")).atrack()
    assert tracksid
    path = Path(log.err_track_dir, f"{tracksid}.log")
    assert path.exists()
    target_part = path.open("r").read().split()[-4]
    assert \
            target_part \
            == "Err(ValErr(\"hello\")).atrack()", \
        target_part
