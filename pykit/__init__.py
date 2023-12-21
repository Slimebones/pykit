import importlib.metadata

from pykit.log import Log, LogMessage

__version__ = importlib.metadata.version("slimebones-pykit")
__all__ = [
    "Log",
    "LogMessage",
]
