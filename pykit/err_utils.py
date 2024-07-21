import traceback

from pykit.code import Code
from pykit.err import ErrDto
from pykit.obj import get_fqname
from pykit.res import Err, Ok, Res


def create_err_dto(cls, err: Exception) -> Res[ErrDto]:
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
