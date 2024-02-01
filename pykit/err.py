from typing import Any
from fcode import code

@code("pykit.not-found-err")
class NotFoundErr(Exception):
    def __init__(self, s: Any, used_search_opts: dict | None = None):
        msg = f"{s} is not found"
        if used_search_opts:
            msg += f", for opts: {used_search_opts}"
        super().__init__(msg)

@code("pykit.already-processed-err")
class AlreadyProcessedErr(Exception):
    def __init__(self, s: Any):
        super().__init__(f"{s} is already processed")

@code("pykit.unsupported-err")
class UnsupportedErr(Exception):
    """
    Some value is not recozniged/supported by the system.
    """
    def __init__(
        self,
        s: Any
    ) -> None:
        msg = f"{s} is unsupported"
        super().__init__(msg)

@code("pykit.inp-err")
class InpErr(Exception):
    def __init__(self, s: Any):
        super().__init__(f"{s} is invalid input")

