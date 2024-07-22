from typing import Generic

from pydantic.generics import GenericModel

from pykit.types import T


class Ptr(GenericModel, Generic[T]):
    """
    Points to some target.
    """
    target: T

    class Config:
        arbitrary_types_allowed = True

