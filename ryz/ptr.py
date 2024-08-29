from typing import Generic, TypeVar

from pydantic.generics import GenericModel

from ryz.types import T


class ptr(GenericModel, Generic[T]):
    """
    Points to some target.
    """
    target: T

    class Config:
        arbitrary_types_allowed = True
