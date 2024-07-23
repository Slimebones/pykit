import traceback

from pykit.code import Code
from pykit.err import ErrDto
from pykit.obj import get_fqname
from pykit.res import Err, Ok, Res


def get_traceback_str(err: Exception) -> str | None:
    s = None
    tb = err.__traceback__
    if tb:
        extracted_list = traceback.extract_tb(tb)
        s = ""
        for item in traceback.StackSummary.from_list(
                extracted_list).format():
            s += item
    return s

def get_msg(err: Exception) -> str:
    return ", ".join([str(a) for a in err.args])

def create_err_dto(err: Exception) -> Res[ErrDto]:
    name = get_fqname(err)
    msg = get_msg(err)
    stacktrace = get_traceback_str(err)
    errcode_res = Code.get_from_type(type(err))
    if isinstance(errcode_res, Err):
        return errcode_res

    return Ok(ErrDto(
        errcode=errcode_res.okval,
        msg=msg,
        name=name,
        stacktrace=stacktrace))
