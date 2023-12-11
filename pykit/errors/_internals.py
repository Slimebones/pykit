from typing import Any


class InternalStringUtils:
    """
    Internal for errors version of string utils to avoid circular imports.
    """
    @staticmethod
    def stringify(value: dict, separator: str = ", ") -> str:
        """
        Transforms dictionary into string representation.
        """
        option_strs: list[str] = []

        for k, v in value.items():
            option_strs.append(f"{k} {v}")

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
