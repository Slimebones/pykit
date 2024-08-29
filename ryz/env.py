import os

from ryz.core import Err, Ok, Res, ecode


def get(key: str, default: str | None = None) -> Res[str]:
    s = os.environ.get(key, default)
    if s is None:
        return Err(f"cannot find environ {key}", ecode.NotFound)
    return Ok(s)

def get_bool(key: str, default: str | None = None) -> Res[bool]:
    env_val = get(key, default)
    if isinstance(env_val, Err):
        return env_val
    env_val = env_val.ok

    match env_val:
        case "0":
            return Ok(False)
        case "1":
            return Ok(True)
        case _:
            return Err(
                f"{key} expected to be \"1\" or \"0\", but got {env_val}",
            )
