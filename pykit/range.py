from typing import Generic, Iterable, TypeVar

T = TypeVar("T")
class Range(Generic[T]):
    """
    Represents range between min and max values.

    Min and Max are always both inclusive.
    """
    def __init__(self, min_: T, max_: T):
        self.min = min_
        self.max = max_

    def get_python_range(self) -> Iterable[T]:
        return range(self.min, self.max + 1)  # type: ignore

    def contains(self, val: T) -> bool:
        return self.min <= val and val <= self.max  # type: ignore
