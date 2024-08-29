from pathlib import Path

from ryz import log
from ryz.core import ValErr
from ryz.core import Err


def test_main():
    tracksid = Err(("hello")).track()
    assert tracksid
    path = Path(log.err_track_dir, f"{tracksid}.log")
    assert path.exists()
    target_part = path.open("r").read().split()[-4]
    assert \
            target_part \
            == "Err((\"hello\")).track()", \
        target_part

async def test_async():
    tracksid = await Err(("hello")).atrack()
    assert tracksid
    path = Path(log.err_track_dir, f"{tracksid}.log")
    assert path.exists()
    target_part = path.open("r").read().split()[-4]
    assert \
            target_part \
            == "Err((\"hello\")).atrack()", \
        target_part
