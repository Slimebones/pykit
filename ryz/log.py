import sys
import tempfile
import traceback
import typing
from pathlib import Path
from typing import Any, NoReturn

from aiofile import async_open
from loguru import logger as _logger

from ryz.obj import get_fqname
from ryz.uuid import uuid4


err_track_dir: Path = Path(tempfile.gettempdir(), "ryz_err_track_dir")
is_debug: bool = False
std_verbosity: int = 1
"""
Verbosity level for stdout/stderr.

For all other targets verbosity is not applied - all msgs are passed to
the sink as it is (yet then it can be blocked there according to the
sink's configuration).

Levels:
    0. silent
    1. cozy chatter
    2. rap god

Methods that produce logging accept variable "v" which defines the
minimal level of verbosity required to make the intended log. For example
if "info('hello', v=1)", the info message would only be produced on
verbosity level 1 or 2.

For debug logs verbosity level is unavailable - they must be emitted
always for their level.
"""

def debug(*args, sep: str = ", "):
    if is_debug:
        _logger.debug(sep.join([str(arg) for arg in args]))

def info(msg: Any, v: int = 1):
    if v < 1:
        return
    if std_verbosity >= v:
        _logger.info(msg)

def warn(msg: Any, v: int = 1):
    if v < 1:
        return
    if std_verbosity >= v:
        _logger.warning(msg)

def err(msg: Any, v: int = 1):
    if v < 1:
        return
    if std_verbosity >= v:
        _logger.error(msg)

def catch(err: Exception, v: int = 1):
    if v < 1:
        return
    if std_verbosity >= v:
        _logger.exception(err)

def err_or_catch(
    err_: Exception, catch_if_v_equal_or_more: int,
):
    if std_verbosity >= catch_if_v_equal_or_more:
        catch(err_)
        return
    err(err)

def fatal(msg: Any, *, exit_code: int = 1) -> NoReturn:
    err(f"FATAL({exit_code}) :: {msg}")
    sys.exit(exit_code)

def _try_get_err_traceback_str(err: Exception) -> str | None:
    """
    Copy of err_utils.try_get_traceback_str to avoid circulars.
    """
    s = None
    tb = err.__traceback__
    if tb:
        extracted_list = traceback.extract_tb(tb)
        s = ""
        for item in traceback.StackSummary.from_list(
                extracted_list).format():
            s += item
    return s

def _get_track_data(
    err_: Exception,
    msg: Any,
    v: int = 1
) -> tuple[str, Path, str, str]:
    msg = str(msg)
    err_track_dir.mkdir(parents=True, exist_ok=True)
    sid = uuid4()
    track_path = Path(err_track_dir, f"{sid}.log")

    err_ = typing.cast(Exception, err_)
    file_content = _try_get_err_traceback_str(err_)

    if not file_content:
        file_content = ""
    # for filled file_content, append newline operator to separate
    # traceback from err dscr
    elif not file_content.endswith("\n"):
        file_content += "\n"

    # add err dscr
    err_msg = _get_msg(err_)
    err_dscr = get_fqname(err_)
    if err_msg:
        err_dscr += ": " + err_msg
    file_content += err_dscr
    final_msg = msg + f"; {err_dscr}" + f"; $track::{track_path}"

    return sid, track_path, file_content, final_msg

def track(
    err_: Exception,
    msg: Any = "tracked",
    v: int = 1
) -> str | None:
    """
    Tracks an err with attached msg.

    The err traceback is written to <log.err_track_dir>/<sid>.log, and the
    msg is logged with the sid. This allows to find out error's traceback
    in a separate file by the original log message.

    If ``v`` parameter doesn't match current verbosity, nothing will be
    done.

    If provided err object is Trackable, the complete track file content
    will be retrieved from err.get_track_file_content().

    Returns tracksid or None.
    """
    if std_verbosity < v:
        return None

    sid, track_path, file_content, final_msg = _get_track_data(
        err_, msg, v)

    with track_path.open("w+") as f:
        f.write(file_content)
    err(final_msg, v)
    return sid

async def atrack(
    err_: Exception,
    msg: Any = "tracked",
    v: int = 1
) -> str | None:
    """
    Asynchronous version of ``log.track``.
    """
    if std_verbosity < v:
        return None

    sid, track_path, file_content, final_msg = _get_track_data(
        err_, msg, v
    )

    async with async_open(track_path, "w+") as f:
        await f.write(file_content)
    err(final_msg, v)
    return sid

@staticmethod
def _get_msg(err_: Exception) -> str:
    return ", ".join([str(a) for a in err_.args])
