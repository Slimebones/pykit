from typing import Generic

from pydantic.generics import GenericModel

from sbpykit.errors import (
    NotFoundError,
)
from sbpykit.expectation import Expectation
from sbpykit.types import T


class DatabaseSearch(GenericModel, Generic[T]):
    """
    Search terms to find database's objects.

    Should be subclassed in order to add extra search terms and specific
    database type-related fields.

    @abstract
    """
    ids: list[str] | None = None
    expectation: Expectation | None = None

    def get_not_found_error(self, title: str) -> NotFoundError:
        return NotFoundError(
            title=title,
            options=self.dict(),
        )
