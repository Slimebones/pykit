import os

import typing_extensions

from ryz.cls import Static
from ryz.core import Err, Ok, Res

def getenv(key: str, default: str | None = None) -> Res[str]:
    s = os.environ.get(key, default)
    if s is None:
        return Err(f"cannot find environ {key}")
    return Ok(s)

def getenv_bool(key: str, default: str | None = None) -> Res[bool]:
    env_val = getenv(key, default)

    match env_val:
        case "0":
            return Ok(False)
        case "1":
            return Ok(True)
        case _:
            return Err(
                f"key expected to be \"1\" or \"0\", but got {key} which"
            )
