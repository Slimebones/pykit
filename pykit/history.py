import typing
from typing import Any, Generic, Self, TypeVar

from pykit.check import check
from pykit.dt import DtUtils
from pykit.types import Timestamp

T = TypeVar("T")

class HistoryErr(Exception):
    """
    @abstract
    """

class ItemTypeHistoryErr(HistoryErr):
    """
    Item of the wrong type is given to history object.
    """
    def __init__(
        self,
        *,
        WrongType: type,
        TypeExpect: type,
    ) -> None:
        message: str = \
            f"cannot operate item of type <{WrongType}>," \
            f" the type <{TypeExpect}> is expected"
        super().__init__(message)

class ItemConversionHistoryErr(HistoryErr):
    """
    Cannot convert initially given item to history's main type.
    """
    def __init__(
        self,
        *,
        ItemType: type,
        MainType: type,
    ) -> None:
        message: str = \
            f"cannot convert item of type <{ItemType}> to the history's" \
            f"main type <{MainType}>"
        super().__init__(message)

class EmptyHistoryErr(HistoryErr):
    """
    No history is present.
    """
    def __init__(
        self,
    ) -> None:
        super().__init__("history is empty")

class DuplicateTimestampHistoryErr(HistoryErr):
    """
    An item with the same timestamp is added.
    """
    def __init__(
        self,
        *,
        timestamp: Timestamp,
        item: Any,
    ) -> None:
        message: str = \
            f"item <{item}> cannot be added" \
            f" with duplicate timestamp <{timestamp}>"
        super().__init__(message)

class DuplicateItemHistoryErr(HistoryErr):
    """
    A new item is the same as previous one.
    """
    def __init__(
        self,
        *,
        item: Any,
    ) -> None:
        message: str = \
            f"item <{item}> cannot be added since it is a duplicate of the"\
            " latest one"
        super().__init__(message)

class History(list[list[float | T]], Generic[T]):
    """
    Tracks changes of states by the time.

    Args:
        main_type:
            Signifies which object's type the history is working with.
    """
    @classmethod
    def create(
        cls,
        *items: T,
    ) -> Self:
        h = cls()
        h.add_many(*items)
        return h

    @property
    def latest(self) -> tuple[Timestamp, T]:
        """
        Returns latest timestamp and according item.
        """
        return self.latest_timestamp, self.latest_item

    @property
    def latest_item(self) -> T:
        """
        Returns latest item in the history.

        The latest item is the item with the most recent timestamp.
        """
        self._check_not_empty()
        return typing.cast(T, self[-1][1])

    @property
    def latest_timestamp(self) -> Timestamp:
        self._check_not_empty()
        return check.instance(self[-1][0], float)

    def add_many(
        self,
        *items: T,
    ) -> None:
        """
        Adds multiple items.

        The timestamp for each item is calculated at according addition time.

        Args:
            items:
                Items to add.
        """
        for item in items:
            self.add(item)

    def add(
        self,
        item: T,
    ) -> None:
        timestamp = DtUtils.get_utc_timestamp()
        self.append([timestamp, item])

    def _check_not_empty(self) -> None:
        if len(self) == 0:
            raise EmptyHistoryErr
