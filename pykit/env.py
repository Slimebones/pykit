import os

from pykit.cls import Static
from pykit.errors.expect import StrExpectError
from pykit.errors.main import PleaseDefineError


class EnvUtils(Static):
    @staticmethod
    def get(key: str, default: str | None = None) -> str:
        env_value: str | None = os.environ.get(key, default)

        if (env_value is None):
            raise PleaseDefineError(
                cannot_do="env retrieval",
                please_define=f"env {key}",
            )

        return env_value

    @staticmethod
    def get_bool(key: str, default: str | None = None) -> bool:
        env_value: str = EnvUtils.get(key, default)

        if (env_value == "1"):
            return True
        if (env_value == "0"):
            return False

        raise StrExpectError(
            key,
            "\"1\" or \"0\"",
        )
