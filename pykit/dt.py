from datetime import datetime, timedelta, timezone

from pykit import validation
from pykit.cls import Static
from pykit.types import Delta, Timestamp


class DTUtils(Static):
    @staticmethod
    def get_utc_timestamp() -> Timestamp:
        return datetime.now(timezone.utc).timestamp()

    @staticmethod
    def get_delta_timestamp(delta: Delta) -> Timestamp:
        """
        Calculates delta timestamp from current moment adding given delta in
        seconds.
        """
        validation.validate(delta, Delta)
        return (
            datetime.now(timezone.utc) + timedelta(seconds=delta)
        ).timestamp()
