import os

import typing_extensions

from pykit.cls import Static
from pykit.err import InpErr, NotFoundErr, ValErr
from pykit.res import Err, Ok, Res


@typing_extensions.deprecated("use module-level functions")
class EnvUtils(Static):
    @staticmethod
    def get(key: str, default: str | None = None) -> str:
        env_value: str | None = os.environ.get(key, default)

        if env_value is None:
            raise NotFoundErr(
                f"env {key}",
            )

        return env_value

    @staticmethod
    def get_bool(key: str, default: str | None = None) -> bool:
        env_value: str = EnvUtils.get(key, default)

        if (env_value == "1"):
            return True
        if (env_value == "0"):
            return False

        raise InpErr(
            f"key expected to be \"1\" or \"0\", but got {key} which",
        )

def getenv(key: str, default: str | None = None) -> Res[str]:
    s = os.environ.get(key, default)
    if s is None:
        return Err(ValErr(f"cannot find environ {key}"))
    return Ok(s)

def getenv_bool(key: str, default: str | None = None) -> Res[bool]:
    env_val = getenv(key, default)

    match env_val:
        case "0":
            return Ok(False)
        case "1":
            return Ok(True)
        case _:
            return Err(InpErr(
                f"key expected to be \"1\" or \"0\", but got {key} which"))
