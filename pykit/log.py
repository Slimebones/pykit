from typing import Any, NoReturn
from loguru import logger as _logger

class log:
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

    For debug logs verbosity level is unavailable - doesn't make sense.
    """

    @classmethod
    def debug(cls, *args, sep: str = ", "):
        if cls.is_debug:
            _logger.debug(sep.join([str(arg) for arg in args]))

    @classmethod
    def info(cls, msg: Any, v: int = 1):
        if v < 1:
            return
        if cls.std_verbosity >= v:
            _logger.info(msg)

    @classmethod
    def warn(cls, msg: Any, v: int = 1):
        if v < 1:
            return
        if cls.std_verbosity >= v:
            _logger.warning(msg)

    @classmethod
    def err(cls, msg: Any, v: int = 1):
        if v < 1:
            return
        if cls.std_verbosity >= v:
            _logger.error(msg)

    @classmethod
    def catch(cls, err: Exception, v: int = 1):
        if v < 1:
            return
        if cls.std_verbosity >= v:
            _logger.exception(err)

    @classmethod
    def err_or_catch(cls, err: Exception, catch_if_v_equal_or_more: int):
        if cls.std_verbosity >= catch_if_v_equal_or_more:
            cls.catch(err)
            return
        cls.err(err)

    @classmethod
    def fatal(cls, msg: Any, *, exit_code: int = 1) -> NoReturn:
        log.err(f"FATAL({exit_code}) :: {msg}")
        exit(exit_code)

