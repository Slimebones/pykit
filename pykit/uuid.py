import uuid


def uuid4() -> str:
    """Creates unique id.

    Returns:
        Id created.
    """
    return uuid.uuid4().hex
