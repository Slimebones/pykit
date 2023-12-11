import os

from pydantic import BaseModel

from pykit.cls import Static
from pykit.errors.expect import StrExpectError
from pykit.errors.main import PleaseDefineError


class EnvSpec(BaseModel):
    """
    Specification of an environment variable.
    """
    key: str
    default: str | None = None
    """
    Default value of env.

    If None, it means that the env is required.
    """


class EnvUtils(Static):
    @staticmethod
    def get(spec: EnvSpec) -> str:
        env_value: str | None = os.environ.get(spec.key, spec.default)

        if (env_value is None):
            raise PleaseDefineError(
                cannot_do="env retrieval",
                please_define=f"env {spec.key}",
            )

        return env_value

    @staticmethod
    def get_bool(spec: EnvSpec) -> bool:
        env_value: str = EnvUtils.get(spec)

        if (env_value == "1"):
            return True
        if (env_value == "0"):
            return False

        raise StrExpectError(
            spec.key,
            "\"1\" or \"0\"",
        )
