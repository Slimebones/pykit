from typing import Generic, Self, TypeVar

ObjectType = TypeVar("ObjectType")
class ObjectInfo(tuple, Generic[ObjectType]):
    """
    Describes an object and it's title.
    """
    __slots__ = ()
    _MAX_LENGTH: int = 2

    # we break inheritance principle by limiting accepting argument from
    # Iterable to tuple[...], but i haven't found any way to specify which
    # types i need within my iterable argument without setting it to tuple
    def __new__(cls, _tuple: tuple[str, ObjectType] = ...) -> Self:
        tuple_length: int = len(list(_tuple))
        if tuple_length > cls._MAX_LENGTH:
            raise ValueError(  # noqa: TRY003
                f"expected length less or equal than <{cls._MAX_LENGTH}>,"
                f" got <{tuple_length}>",
            )

        return super().__new__(cls, _tuple)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"{self[0]}=<{self[1]}>"
