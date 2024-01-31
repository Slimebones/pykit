from typing import Any
from loguru import logger as _logger

class log:
    verbosity: int = 0
    """
    Verbosity level.

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
        _logger.debug(sep.join(args))

    @classmethod
    def info(cls, msg: Any, v: int = 0):
        if cls.verbosity >= v:
            _logger.info(msg)

    @classmethod
    def warn(cls, msg: Any, v: int = 0):
        if cls.verbosity >= v:
            _logger.warning(msg)

    @classmethod
    def err(cls, msg: Any, v: int = 0):
        if cls.verbosity >= v:
            _logger.error(msg)

    @classmethod
    def catch(cls, err: Exception, v: int = 0):
        if cls.verbosity >= v:
            _logger.exception(err)

    @classmethod
    def err_or_catch(cls, err: Exception, catch_if_v_equal_or_more: int):
        if cls.verbosity >= catch_if_v_equal_or_more:
            cls.catch(err)
            return
        cls.err(err)

