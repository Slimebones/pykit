"""
Manages data objects marking.

Why do we need to mark data objects? Because, e.g., we want to send it to
archive.
"""
from typing import Any, Awaitable, Callable

from pykit.check import check
from pykit.err import InpErr
from pykit.query import UpdQuery
from pykit.types import T


class MarkErr(Exception):
    pass

class MarkUtils:
    @classmethod
    def has(cls, mark: str, obj: Any) -> bool:
        return mark in cls.get_marks(obj)

    @classmethod
    def add(
        cls,
        mark: str,
        obj: Any,
    ):
        marks = cls.get_marks(obj)
        if mark in marks:
            raise MarkErr(
                f"mark {mark} already presented in obj {obj} marks {marks}",
            )
        marks.append(mark)

    @classmethod
    def remove(
        cls,
        mark: str,
        obj: Any,
    ):
        marks = cls.get_marks(obj)
        if mark not in marks:
            raise MarkErr(
                f"cannot del: no such mark {mark} in obj {obj} marks {marks}",
            )
        marks.remove(mark)

    @classmethod
    def get_push_uq(
        cls,
        mark: str,
        obj: Any,
    ) -> UpdQuery:
        marks = cls.get_marks(obj)
        if mark in marks:
            raise MarkErr(
                f"mark {mark} already presented in obj {obj} marks {marks}",
            )
        return UpdQuery.create(push={
            "internal_marks": mark,
        })

    @classmethod
    def get_pull_uq(
        cls,
        mark: str,
        obj: Any,
    ) -> UpdQuery:
        marks = cls.get_marks(obj)
        if mark not in marks:
            raise MarkErr(
                f"cannot del: no such mark {mark} in obj {obj} marks {marks}",
            )
        return UpdQuery.create(pull={
            "internal_marks": mark,
        })

    @classmethod
    async def decide(
        cls,
        mark: str,
        obj: T,
        *,
        on_has: Callable[[str, T], Awaitable[None]] | None = None,
        on_missing: Callable[[str, T], Awaitable[None]] | None = None,
    ):
        """
        Call on_has or on_missing depending on fact that obj has/hasnt the
        mark.
        """
        if not on_has and not on_missing:
            raise InpErr("non-specified on_has and on_missing corofns")

        has = cls.has(mark, obj)

        if on_has and has:
            await on_has(mark, obj)
            return
        if on_missing:
            await on_missing(mark, obj)

    @classmethod
    def get_marks(cls, obj: Any) -> list[str]:
        try:
            marks: list[str] = obj.internal_marks
        except AttributeError as err:
            raise MarkErr(f"obj {obj} is not marked") from err

        check.instance(marks, list)
        return list(check.each_instance(marks, str))

