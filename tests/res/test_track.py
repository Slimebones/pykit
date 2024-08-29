from pathlib import Path

from ryz import log
from ryz.core import Err


def test_main():
    tracksid = Err("hello").track()
    assert tracksid
    path = Path(log.err_track_dir, f"{tracksid}.log")
    assert path.exists()
    content = path.open("r").read()
    target_part = content.split()[-1]
    assert target_part == "hello"

async def test_async():
    tracksid = await Err("hello").atrack()
    assert tracksid
    path = Path(log.err_track_dir, f"{tracksid}.log")
    assert path.exists()
    content = path.open("r").read()
    target_part = content.split()[-1]
    assert target_part == "hello"
