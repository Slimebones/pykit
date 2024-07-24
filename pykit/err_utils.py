
from pykit.code import Code
from pykit.err import ErrDto
from pykit.obj import get_fqname
from pykit.res import Err, Ok, Res
from pykit.tb import get_traceback_str


def get_err_msg(err: Exception) -> str:
    return ", ".join([str(a) for a in err.args])

def get_err_dscr(err: Exception) -> str:
    err_msg = get_err_msg(err)
    err_dscr = get_fqname(err)
    if err_msg:
        err_dscr += ": " + err_msg
    return err_dscr

async def create_err_dto(err: Exception) -> Res[ErrDto]:
    name = get_fqname(err)
    msg = get_err_msg(err)
    stacktrace = get_traceback_str(err)
    errcode_res = await Code.get_regd_code_by_type(type(err))
    if isinstance(errcode_res, Err):
        return errcode_res

    return Ok(ErrDto(
        errcode=errcode_res.okval,
        msg=msg,
        name=name,
        stacktrace=stacktrace))
