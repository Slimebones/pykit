"""
Additional utils for error handling.
"""
import re
from typing import Any


def stringify(value: dict, separator: str = ", ") -> str:
    """
    Transforms dictionary into string representation.
    """
    option_strs: list[str] = []

    for k, v in value.items():
        option_strs.append(f"{k}={v}")

    return separator.join(option_strs)


def get_titled_value(
    title: str,
    value: Any | None = None,
) -> str:
    titled_value: str = title
    if value:
        titled_value = f"{title} <{value!s}>"

    return titled_value
