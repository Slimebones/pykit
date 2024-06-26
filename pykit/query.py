"""
Manage mongo-like queries.
"""
import typing
from typing import Any, Iterable, Literal, Self

from pymongo.collection import Collection
from pymongo.command_cursor import CommandCursor
from result import Err, Ok

from pykit.check import check
from pykit.err import NotFoundErr, ValueErr
from pykit.log import log
from pykit.res import Res, raise_err_val

QueryUpdOperator = Literal[
    "$set", "$unset", "$inc", "$pull", "$pop", "$push", "$mul"]
QueryUpdOperators = [
    "$set",
    "$unset",
    "$inc",
    "$pull",
    "$pop",
    "$push",
    "$mul"]

class Query(dict[str, Any]):
    def __init__(self, inp):
        super().__init__(inp)
        raise_err_val(self.check)

    def copy(self) -> Self:
        return typing.cast(Self, Query(super().copy()))

    def check(self) -> Res[None]:
        """
        Checks query to be valid.
        """
        return Ok(None)

    def _check_disallowed_keys(
            self,
            disallowed_keys: Iterable[str]):
        for disallowed_key in disallowed_keys:
            if disallowed_key.startswith("$"):
                raise ValueErr(
                    f"cannot disallow upd operators (passed {disallowed_key})")

    def disallow(
        self,
        *disallowed_keys: str,
        raise_mode: Literal["null", "warn", "err"] = "null",
    ) -> Self:
        """
        Process this query for disallowed keys.

        Each disallowed key will be scheduled for delete, but if raise_mode
        is not "err".
        """
        query = self.copy()
        keys_to_del: list[str] = []
        ikeys_to_del: dict[QueryUpdOperator, str] = {}

        self._check_disallowed_keys(disallowed_keys)

        for k, v in query.items():
            if k in QueryUpdOperators:
                if not isinstance(v, dict):
                    raise ValueErr(f"for operator {k}, val {v} should be dict")
                for ik in v:
                    if ik in disallowed_keys:
                        ikeys_to_del[typing.cast(QueryUpdOperator, k)] = ik
                        self._raise_err_for_disallowed(ik, raise_mode)
                continue
            if k in disallowed_keys:
                keys_to_del.append(k)
                self._raise_err_for_disallowed(k, raise_mode)

        for k in keys_to_del:
            del query[k]
        for operator, ik in ikeys_to_del.items():
            del query[operator][ik]

        return query

    def _raise_err_for_disallowed(
        self,
        key: str,
        raise_mode: Literal["null", "warn", "err"],
        ):
        match raise_mode:
            case "null":
                return
            case "warn":
                log.warn(
                    f"{key} is not allowed in query {self} => skip",
                )
            case "err":
                raise ValueErr(f"{key} in query {self}")
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
        unset: dict[str, Any] | None = None,
    ) -> Self:
        return typing.cast(Self, Query({
            "$set": set or {},
            "$inc": inc or {},
            "$push": push or {},
            "$pull": pull or {},
            "$pop": pop or {},
            "$unset": unset or {},
        }))

    def check(self) -> Res[None]:
        for k in self.keys():
            if k not in QueryUpdOperators:
                return Err(ValueErr(f"query {self} is incorrect to be updq"))
        return Ok(None)

    def get_operator_val(self, key: str) -> Res[dict[str, Any]]:
        """
        Gets top-level upd operator.
        """
        if not key.startswith("$"):
            raise ValueErr(f"invalid upd operator key: {key}")

        res_check = self.check()
        if isinstance(res_check, Err):
            return res_check

        for k, v in self.items():
            if k == key:
                if not isinstance(v, dict):
                    return Err(ValueErr(
                        f"upd operator {k} should have dict val,"
                        f" got {v} instead"))
                return Ok(v)

        return Err(NotFoundErr(
            f"field with key={key} is not found in upd query {self}"))

class AggQuery(Query):
    @classmethod
    def create(cls, *stages: dict[str, Any]) -> Self:
        return cls({
            "pipeline": list(stages),
        })

    def check(self) -> Res[None]:
        if "pipeline" not in self:
            self["pipeline"] = []
        if len(self) != 1:
            return Err(ValueErr(
                f"query {self} is incorrect to be aggq"))
        pipeline = self["pipeline"]
        if not isinstance(pipeline, list):
            return Err(ValueErr(
                f"pipeline {pipeline} must be list"))
        for stage in pipeline:
            if not isinstance(stage, dict):
                return Err(ValueErr(
                    f"stage {stage} must be dict"))
            for k in stage:
                if not isinstance(k, str):
                    return Err(ValueErr(
                        f"stage key {k} must be str"))
                if not k.startswith("$"):
                    return Err(ValueErr(
                        f"query {self} is incorrect to be aggq"))
        return Ok(None)

    def get_pipeline(self, *, _has_check: bool = True) -> list[dict[str, Any]]:
        if _has_check:
            self.check().unwrap()
        return self["pipeline"]

    def apply(self, collection: Collection) -> CommandCursor:
        self.check().unwrap()
        return collection.aggregate(self.get_pipeline(_has_check=False))
