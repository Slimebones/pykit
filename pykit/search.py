from typing import Generic

from pydantic.generics import GenericModel

from pykit.expectation import Expectation
from pykit.types import T


class DbSearch(GenericModel, Generic[T]):
    """
    Search terms to find database's objects.

    Should be subclassed in order to add extra search terms and specific
    database type-related fields.

    @abs
    """
    sids: list[str] | None = None
    expectation: Expectation | None = None

