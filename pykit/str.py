import re
from typing import Any

from pykit.cls import Static


class StringUtils(Static):
    @staticmethod
    def stringify(value: dict, separator: str = ", ") -> str:
        """
        Transforms dictionary into string representation.
        """
        option_strs: list[str] = []

        for k, v in value.items():
            option_strs.append(f"{k}={v}")

        return separator.join(option_strs)

    @staticmethod
    def get_titled_value(
        title: str,
        value: Any | None = None,
    ) -> str:
        titled_value: str = title
        if value:
            titled_value = f"{title} <{value!s}>"

        return titled_value

    @staticmethod
    def has_cyrillic(text: str) -> bool:
        """
        Checks if text contains any Cyrillic characters.
        """
        return bool(re.search("[а-яА-Я]", text))

    @staticmethod
    def remove_non_alpha(s: str) -> str:
        """
        Remove all non-alpha characters from string.
        """
        # https://stackoverflow.com/a/22521156
        regex = re.compile("[^a-zA-Z]")
        return regex.sub("", s)

    @staticmethod
    def remove_non_alnum(s: str) -> str:
        """
        Remove all non-alpha characters from string.
        """
        # https://stackoverflow.com/a/22521156
        regex = re.compile("[^a-zA-Z0-9]")
        return regex.sub("", s)
