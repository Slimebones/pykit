
from pydantic import BaseModel


class ErrDto(BaseModel):
    """
    Represents an error as data transfer object.

    "stacktrace" used to comply with other languages structures, for Python
    it's actually a traceback.
    """
    name: str
    errcode: str
    """
    ErrDto works only with coded errors.
    """
    msg: str
    stacktrace: str | None = None

    @staticmethod
    def code() -> str:
        return "err"

class ValErr(ValueError):
    @staticmethod
    def code() -> str:
        return "val_err"

class NotFoundErr(Exception):
    @staticmethod
    def code() -> str:
        return "not_found_err"

class AlreadyProcessedErr(Exception):
    @staticmethod
    def code() -> str:
        return "already_processed_err"

class UnsupportedErr(Exception):
    """
    Some value is not recozniged/supported by the system.
    """
    @staticmethod
    def code() -> str:
        return "unsupported_err"

class InpErr(Exception):
    """
    A problem with received input.
    """
    @staticmethod
    def code() -> str:
        return "inp_err"

class LockErr(Exception):
    @staticmethod
    def code() -> str:
        return "lock_err"
