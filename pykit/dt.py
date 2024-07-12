import time

import typing_extensions

from pykit.cls import Static
from pykit.types import Delta, Timestamp


@typing_extensions.deprecated("use module \"t\"")
class DtUtils(Static):
    @staticmethod
    def get_utc_timestamp() -> Timestamp:
        return time.time()

    @staticmethod
    def get_delta_timestamp(delta: Delta) -> Timestamp:
        """
        Calculates delta timestamp from current moment adding given delta in
        seconds.
        """
        return time.time() + delta
