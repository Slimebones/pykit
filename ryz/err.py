from pydantic import BaseModel


class Error(Exception):
    """
    Represents an error as data transfer object.

    "stacktrace" used to comply with other languages structures, for Python
    it's actually a traceback.
    """
    def __init__(self, code: str = "err", msg: str | None = None) -> None:
        self.code = code
        self.msg = msg
        final = code
        if msg:
            final += ": " + msg
        super().__init__(final)

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
