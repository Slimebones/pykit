import os

from pykit.cls import Static
from pykit.err import InpErr, NotFoundErr


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
