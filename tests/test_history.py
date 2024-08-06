from enum import Enum
from typing import TYPE_CHECKING

from ryz.check import check
from ryz.dt import DtUtils
from ryz.history import (
    EmptyHistoryErr,
    History,
)

if TYPE_CHECKING:
    from ryz.types import Timestamp


class _Color(Enum):
    Red = "red"
    Blue = "blue"
    Green = "green"
    Yellow = "yellow"

def test_empty():
    history: History[_Color] = History()

    check.expect(
        lambda: history.latest,
        EmptyHistoryErr,
    )

def test_add():
    history: History[_Color] = History()

    history.add_many(
        _Color.Red,
        _Color.Blue,
    )

    after_timestamp: Timestamp = DtUtils.get_utc_timestamp()

    # "<=" since sometimes timestamps are evaluated as equal
    assert history.latest_timestamp <= after_timestamp
    assert history.latest_item is _Color.Blue
