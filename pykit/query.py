"""
Manage queries! Too much queries!
"""
from typing import Literal

from pykit.checking import check
from pykit.err import InpErr
from pykit.log import log


class QueryUtils:
    """
    Note that if method name starts with "process_query" it probably means
    that the incoming query will be changed. So consider copying it before
    passing to the methods.
    """

    @classmethod
    def process_query_for_disallowed(
        cls,
        query: dict,
        disallowed_keys: list[str],
        *,
        raise_mod: Literal["null", "warn", "err"] = "null"
    ):
        """
        Process incoming query for disallowed keys.

        Each disallowed key will be scheduled for delete, but if raise_mod
        is not "err".
        """

        keys_to_del: list[str] = []

        for k, v in query.items():
            if k in disallowed_keys:
                keys_to_del.append(k)
                cls._raise_err_for_disallowed(k, raise_mod)

        for k in keys_to_del:
            del query[k]

    @classmethod
    def _raise_err_for_disallowed(
        cls,
        key: str,
        raise_mod: Literal["null", "warn", "err"]
        ):
        match raise_mod:
            case "null":
                return
            case "warn":
                log.warn(
                    f"{key} is not allowed in query => skip"
                )
            case "err":
                raise InpErr(f"{key} in query")
            case _:
                check.fail()


