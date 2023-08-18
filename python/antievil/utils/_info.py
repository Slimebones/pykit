from collections.abc import Iterable
from typing import Any, Generic, Self, TypeVar


ObjectType = TypeVar("ObjectType")
class ObjectInfo(tuple, Generic[ObjectType]):
    """
    Describes an object and it's title.
    """
    def __new__(cls, __iterable: Iterable = ...) -> Self:
        iterable_length: int = len(list(__iterable))
        if iterable_length > 2:
            raise ValueError(
                "expected length less or equal than <2>,"
                f" got <{iterable_length}>"
            )

        return super().__new__(cls, __iterable)

    # def __str__(self) -> str:
    #     return self.__repr__()

    # def __repr__(self) -> str:
    #     return f""

a = ObjectInfo[int]([1, 2, 3])
print(a)
