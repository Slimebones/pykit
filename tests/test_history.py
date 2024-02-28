from enum import Enum
from typing import TYPE_CHECKING

from pykit.check import check
from pykit.dt import DtUtils
from pykit.history import (
    DuplicateItemHistoryErr,
    EmptyHistoryErr,
    History,
    ItemTypeHistoryErr,
)

if TYPE_CHECKING:
    from pykit.types import Timestamp


class _Color(Enum):
    Red = "red"
    Blue = "blue"
    Green = "green"
    Yellow = "yellow"

def test_empty():
    history: History[_Color] = History(_Color)

    check.expect(
        lambda: history.latest,
        EmptyHistoryErr,
    )

def test_add():
    history: History[_Color] = History(_Color)

    history.add(
        _Color.Red,
        _Color.Blue,
    )

    after_timestamp: Timestamp = DtUtils.get_utc_timestamp()

    assert history.latest_timestamp < after_timestamp
    assert history.latest_item is _Color.Blue

def test_add_wrong_type():
    history: History[_Color] = History(_Color)

    history.add(_Color.Red)

    check.expect(
        history.add,
        ItemTypeHistoryErr,
        10,
    )

def test_add_item_duplicates():
    history: History[_Color] = History(_Color)

    check.expect(
        history.add,
        DuplicateItemHistoryErr,
        _Color.Red,
        _Color.Red,
    )
