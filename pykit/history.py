from enum import Enum
from typing import Any, Generic, Literal, Self, TypeVar

from pykit.dt import DtUtils
from pykit.types import Timestamp

T = TypeVar("T")

class HistoryError(Exception):
    """
    @abstract
    """

class ItemTypeHistoryError(HistoryError):
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

class ItemConversionError(HistoryError):
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

class EmptyHistoryError(HistoryError):
    """
    No history is present.
    """
    def __init__(
        self,
    ) -> None:
        super().__init__("history is empty")

class DuplicateTimestampHistoryError(HistoryError):
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

class DuplicateItemHistoryError(HistoryError):
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

class History(Generic[T]):
    """
    Tracks changes of states by the time.

    Args:
        main_type:
            Signifies which object's type the history is working with.
    """
    def __init__(
        self,
        main_type: type[T],
    ):
        self._main_type = main_type
        self._data: list[tuple[float, T]] = []

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
        return self._data[-1][1]

    @property
    def latest_timestamp(self) -> Timestamp:
        self._check_not_empty()
        return self._data[-1][0]

    def add(
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
            self._add_one(item)

    def _add_one(
        self,
        item: T,
    ) -> None:
        timestamp = DtUtils.get_utc_timestamp()
        self._check_item_duplicates(item)
        self._check_item_type(item)
        self._data.append((timestamp, item))

    def _check_not_empty(self) -> None:
        if not self._data:
            raise EmptyHistoryError()

    def _check_item_duplicates(
        self,
        item: T,
    ) -> None:
        """
        Checks that the item is not the same as the latest added one.
        """
        try:
            self._check_not_empty()
        except EmptyHistoryError:
            # nothing to do with duplicates if the history is empty
            return
        else:
            latest_item: T = self.latest_item

            # check both value and reference equality
            if item is latest_item or item == latest_item:
                raise DuplicateItemHistoryError(
                    item=item,
                )

    def _check_item_type(
        self,
        item: T,
    ) -> None:
        """
        Checks if item type is the same as history's main type.
        """
        ItemType: type = type(item)

        if ItemType is not self._main_type:
            raise ItemTypeHistoryError(
                WrongType=ItemType,
                TypeExpect=self._main_type,
            )
        else:
            return
