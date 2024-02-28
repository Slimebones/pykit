"""
Manage queries! Too much queries!
"""
from typing import Literal, Self

from pykit.checking import check
from pykit.err import InpErr
from pykit.log import log


class Query(dict):
    def disallow(
        self,
        disallowed_keys: list[str],
        *,
        raise_mod: Literal["null", "warn", "err"] = "null",
    ) -> Self:
        """
        Process this query for disallowed keys.

        Each disallowed key will be scheduled for delete, but if raise_mod
        is not "err".
        """

        keys_to_del: list[str] = []

        for k in self:
            if k in disallowed_keys:
                keys_to_del.append(k)
                self._raise_err_for_disallowed(k, raise_mod)

        for k in keys_to_del:
            del self[k]

        return self

    def _raise_err_for_disallowed(
        self,
        key: str,
        raise_mod: Literal["null", "warn", "err"],
        ):
        match raise_mod:
            case "null":
                return
            case "warn":
                log.warn(
                    f"{key} is not allowed in query => skip",
                )
            case "err":
                raise InpErr(f"{key} in query")
            case _:
                check.fail()

