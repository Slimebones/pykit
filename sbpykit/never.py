from typing import Never, NoReturn

from sbpykit.errors.main import LogicError


def never(_: Never) -> NoReturn:
    error_message: str = "unhandled case"
    raise LogicError(error_message)
