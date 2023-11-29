import uuid

from sbpykit.klass import Static


class RandomUtils(Static):
    @staticmethod
    def makeid() -> str:
        """Creates unique id.

        Returns:
            Id created.
        """
        return uuid.uuid4().hex
