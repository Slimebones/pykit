import traceback
from typing import Self

from pydantic import BaseModel

from pykit.code import Code
from pykit.obj import get_fqname
from pykit.res import Err, Ok, Res, is_err


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

    @classmethod
    def create(cls, err: Exception) -> Res[Self]:
        name = get_fqname(err)
        msg = ", ".join([str(a) for a in err.args])
        stacktrace = None
        tb = err.__traceback__
        if tb:
            extracted_list = traceback.extract_tb(tb)
            stacktrace = ""
            for item in traceback.StackSummary.from_list(
                    extracted_list).format():
                stacktrace += item
        errcode_res = Code.get_from_type(type(err))
        if isinstance(errcode_res, Err):
            return errcode_res

        return Ok(cls(
            errcode=errcode_res.okval,
            msg=msg,
            name=name,
            stacktrace=stacktrace))

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

