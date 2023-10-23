from typing import Generic, Self, TypeVar

ObjectType = TypeVar("ObjectType")
class ObjectInfo(tuple, Generic[ObjectType]):
    """
    Describes an object and it's title.
    """
    __slots__ = ()
    _MIN_LENGTH: int = 1
    _MAX_LENGTH: int = 2

    # we break inheritance principle by limiting accepting argument from
    # Iterable to tuple[...], but i haven't found any way to specify which
    # types i need within my iterable argument without setting it to tuple
    def __new__(
        cls,
        data: Self | tuple[str, ObjectType] | str = ...,
    ) -> Self:

        final_input: tuple[str, ObjectType | None]

        if isinstance(data, cls):
            return data
        elif isinstance(data, tuple):
            tuple_length: int = len(list(data))

            if not cls._MIN_LENGTH <= tuple_length <= cls._MAX_LENGTH:
                raise ValueError(  # noqa: TRY003
                    f"unexpected length <{tuple_length}>",
                )

            final_input = data

        elif isinstance(data, str):
            final_input = (data, None)
        else:
            raise TypeError

        return super().__new__(cls, final_input)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        if self[1] is None:
            return f"{self[0]}"
        return f"{self[0]}=<{self[1]}>"
