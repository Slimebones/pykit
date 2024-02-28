from enum import Enum
from typing import TYPE_CHECKING

from pykit import validation
from pykit.dt import DTUtils

from pycore.history import History
from pycore.history.errors import (
    DuplicateItemHistoryError,
    EmptyHistoryError,
    ItemConversionError,
    ItemTypeHistoryError,
)

if TYPE_CHECKING:
    from pycore.types import Timestamp


class _Color(Enum):
    Red = "red"
    Blue = "blue"
    Green = "green"
    Yellow = "yellow"


def test_empty():
    history: History[_Color] = History(_Color)

    validation.expect(
        lambda: history.latest,
        EmptyHistoryError,
    )


def test_initial_map_creation():
    timestamp1: Timestamp = DTUtils.get_utc_timestamp()
    timestamp2: Timestamp = DTUtils.get_utc_timestamp()

    history: History[_Color] = History(
        _Color,
        initial_map={
            str(timestamp1): _Color.Red,
            str(timestamp2): _Color.Blue,
        },
    )

    assert history.latest_timestamp == timestamp2
    assert history.latest_item is _Color.Blue


def test_add():
    history: History[_Color] = History(_Color)

    history.add(
        _Color.Red,
        _Color.Blue,
    )

    after_timestamp: Timestamp = DTUtils.get_utc_timestamp()

    assert history.latest_timestamp < after_timestamp
    assert history.latest_item is _Color.Blue


def test_add_wrong_type():
    history: History[_Color] = History(_Color)

    history.add(_Color.Red)

    validation.expect(
        history.add,
        ItemTypeHistoryError,
        10,
    )


def test_add_item_duplicates():
    history: History[_Color] = History(_Color)

    validation.expect(
        history.add,
        DuplicateItemHistoryError,
        _Color.Red,
        _Color.Red,
    )


def test_initial_conversion():
    """
    Should convert literal string to the specified enum's fields.
    """
    history: History[_Color] = History(_Color, initial_map={
        str(DTUtils.get_utc_timestamp()): "red",
    })

    assert history.latest_item is _Color.Red


def test_initial_conversion_mongo_timestamps():
    """
    Should convert literal string to the specified enum's fields.
    """
    history: History[_Color] = History(_Color, initial_map={
        str(DTUtils.get_utc_timestamp()).replace(".", "d"): "red",
    })

    assert history.latest_item is _Color.Red


def test_initial_conversion_error():
    validation.expect(
        History,
        ItemConversionError,
        int,
        initial_map={
            str(DTUtils.get_utc_timestamp()): "red",
        },
    )
