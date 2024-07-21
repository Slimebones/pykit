import uuid

import typing_extensions

from pykit.cls import Static


@typing_extensions.deprecated("use uuid::uuid4() instead")
class RandomUtils(Static):
    @staticmethod
    def makeid() -> str:
        """Creates unique id.

        Returns:
            Id created.
        """
        return uuid.uuid4().hex
