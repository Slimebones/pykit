import importlib.metadata as _import_meta

from pykit.check import check
from pykit.log import log

__version__ = _import_meta.version("pykit")
# export only core things here
__all__ = [
    "check",
    "log",
]
