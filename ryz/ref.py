from typing import Generic, TypeVar

T = TypeVar("T")
class Ref(Generic[T]):
    """Stores a value."""
    def __init__(self, val: T) -> None:
        self.val: T = val
