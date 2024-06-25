"""
Manage mongo-like queries.
"""
import typing
from typing import Any, Literal, Self

from pymongo.collection import Collection
from pymongo.command_cursor import CommandCursor

from pykit.check import check
from pykit.err import InpErr, NotFoundErr, ValueErr
from pykit.log import log

QueryUpdOperator = Literal["$set", "$inc", "$pull", "$pop", "$push", "$mul"]
QueryUpdOperators = [
    "$set",
    "$inc",
    "$pull",
    "$pop",
    "$push",
    "$mul"]

class Query(dict[str, Any]):
    def copy(self) -> Self:
        return typing.cast(Self, Query(super().copy()))

    def _check_disallowed_keys(
            self,
            *disallowed_keys: str):
        for disallowed_key in disallowed_keys:
            if disallowed_key.startswith("$"):
                raise ValueErr(
                    f"cannot disallow upd operators (passed {disallowed_key})")

    def disallow(
        self,
        *disallowed_keys: str,
        raise_mod: Literal["null", "warn", "err"] = "null",
    ) -> Self:
        """
        Process this query for disallowed keys.

        Each disallowed key will be scheduled for delete, but if raise_mod
        is not "err".
        """
        query = self.copy()
        keys_to_del: list[str] = []
        ikeys_to_del: dict[QueryUpdOperator, str] = {}

        self._check_disallowed_keys()

        for k, v in query.items():
            if k in QueryUpdOperators:
                if not isinstance(v, dict):
                    raise ValueErr(f"for operator {k}, val {v} should be dict")
                for ik in v:
                    if ik in disallowed_keys:
                        ikeys_to_del[typing.cast(QueryUpdOperator, k)] = ik
                        self._raise_err_for_disallowed(ik, raise_mod)
                continue
            if k in disallowed_keys:
                keys_to_del.append(k)
                self._raise_err_for_disallowed(k, raise_mod)

        for k in keys_to_del:
            del query[k]
        for operator, ik in ikeys_to_del.items():
            del query[operator][ik]

        return query

    def _raise_err_for_disallowed(
        self,
        key: str,
        raise_mod: Literal["null", "warn", "err"],
        ):
        match raise_mod:
            case "null":
                return
            case "warn":
                log.warn(
                    f"{key} is not allowed in query {self} => skip",
                )
            case "err":
                raise InpErr(f"{key} in query {self}")
            case _:
                check.fail()

class SearchQuery(Query):
    @classmethod
    def create_sid(cls, sid: str) -> Self:
        return typing.cast(Self, Query({"sid": sid}))

class UpdQuery(Query):
    @classmethod
    def create(  # noqa: PLR0913
        cls,
        *,
        set: dict[str, Any] | None = None,
        inc: dict[str, Any] | None = None,
        push: dict[str, Any] | None = None,
        pull: dict[str, Any] | None = None,
        pop: dict[str, Any] | None = None,
    ) -> Self:
        return typing.cast(Self, Query({
            "$set": set or {},
            "$inc": inc or {},
            "$push": push or {},
            "$pull": pull or {},
            "$pop": pop or {},
        }))

    def get_upd_field(self, name: str) -> Any:
        for op_k, op_val in self.items():
            if op_k not in QueryUpdOperators:
                raise ValueErr(f"query {self} is incorrect for upd")
            for k, v in op_val.items():
                if k == name:
                    return v
        raise NotFoundErr(
            f"field with name {name} is not found in upd query {self}")

class AggQuery(Query):
    def get_pipeline(self) -> list[dict[str, Any]]:
        if "pipeline" not in self:
            raise ValueErr("undefined pipeline for aggq")
        pipeline = self["pipeline"]
        if (
                not isinstance(pipeline, list)
                or not all(isinstance(item, dict) for item in pipeline)):
            raise ValueErr(f"invalid aggq pipeline composition: {pipeline}")
        return pipeline

    def apply(self, collection: Collection) -> CommandCursor:
        return collection.aggregate(self.get_pipeline())
