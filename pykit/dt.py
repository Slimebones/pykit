from datetime import datetime, timedelta, timezone

from pykit.check import check
from pykit.cls import Static
from pykit.types import Delta, Timestamp


class DtUtils(Static):
    @staticmethod
    def get_utc_timestamp() -> Timestamp:
        return datetime.now(timezone.utc).timestamp()

    @staticmethod
    def get_delta_timestamp(delta: Delta) -> Timestamp:
        """
        Calculates delta timestamp from current moment adding given delta in
        seconds.
        """
        check.instance(delta, Delta)
        return (
            datetime.now(timezone.utc) + timedelta(seconds=delta)
        ).timestamp()
