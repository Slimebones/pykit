from enum import Enum
from typing import Any, Generic, Literal, Self, TypeVar

from pykit.dt import DTUtils
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
        *,
        failed_action: str,
    ) -> None:
        message: str = \
            f"cannot perform action <{failed_action}>: the history is empty"
        super().__init__(message)

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
        MainType:
            Signifies which object's type the history is working with.
        initial_map(optional):
            An existing history map to initialize from. Defaults to None, i.e.
            an empty map will be initialized.
            Note that for the initial map the timestamps are stored in strings
            to comply with MongoDB and spend less processing time on
            string-float convertion. Also the timestamps cannot be stored in
            mongo with dots, so they are replaced by letter "d". They are
            automatically adjusted if occured in initial_map or after
            `mongovalue` property obtaining.
            If initial map value type is not the same, as the history's main
            type, the convertation will be performed, if possible.
    """
    def __init__(
        self,
        MainType: type,
        *,
        initial_map: dict[str, Any] | None = None,
    ):
        self._MainType: type = MainType
        self._map: dict[str, T] = \
            {} if initial_map is None else self._convert_map(initial_map)

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
        return self._map[str(self.latest_timestamp)]

    @property
    def latest_timestamp(self) -> Timestamp:
        self._check_not_empty()
        return sorted([float(k) for k in self._map])[-1]

    @property
    def mongovalue_latest_timestamp(self) -> str:
        return self._adjust_timestamp_to_mongo(str(self.latest_timestamp))

    @property
    def mongovalue(self) -> dict[str, T]:
        adjusted: dict[str, T] = {}

        for k, v in self._map.items():
            adjusted[self._adjust_timestamp_to_mongo(k)] = v

        return adjusted

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
        timestamp: Timestamp = DTUtils.get_utc_timestamp()

        self._check_item_duplicates(item)

        self._check_item_type(item)

        self._map[str(timestamp)] = item

    def _check_not_empty(self) -> None:
        if len(self._map.values()) == 0:
            raise EmptyHistoryError(
                failed_action="get latest",
            )

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

        if ItemType is not self._MainType:
            raise ItemTypeHistoryError(
                WrongType=ItemType,
                TypeExpect=self._MainType,
            )
        else:
            return

    def _convert_map(
        self,
        initial_map: dict[str, Any],
    ) -> dict[str, T]:
        result: dict[str, T] = {}

        for k, v in initial_map.items():
            result[self._adjust_timestamp_from_mongo(k)] = \
                self._convert_item(v)

        return result

    def _convert_item(
        self,
        item: Any,
    ) -> T:
        if isinstance(item, self._MainType):
            return item
        elif issubclass(self._MainType, Enum):
            return self._MainType(item)
        else:
            raise ItemConversionError(
                ItemType=type(item),
                MainType=self._MainType,
            )

    def _adjust_timestamp_to_mongo(self, timestamp: str) -> str:
        return timestamp.replace(".", "d")


    def _adjust_timestamp_from_mongo(self, timestamp: str) -> str:
        return timestamp.replace("d", ".")
