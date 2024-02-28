from copy import deepcopy
from typing import Any

import dictdiffer
from benedict import benedict

from pykit import validation
from pykit.cls import Static
from pykit.errors import NotFoundError
from pykit.errors.main import EmptyInputError

"""
Dict++ - improved dictionary based on benedict.
"""
dictpp = benedict


class MapUtils(Static):
    @staticmethod
    def find(location: str, mp: dict) -> Any:
        """Finds field by location.

        Args:
            location:
                String representing location to search from in format
                "key1.key2.key3".
            mp:
                Dict to search in.

        Returns:
            Field found.
        """
        validation.validate(location, str)
        validation.validate(mp, dict)

        return dictpp(mp)[location]

    @staticmethod
    def patch(
        to_be_patched: dict,
        source: dict,
        should_deepcopy: bool = True,
    ) -> dict:
        """Patch one dictionary by another.

        Args:
            to_be_patched:
                Dict to be patched.
            source:
                Source dict to use for patching.
            should_deepcopy (optional):
                Whether deepcopy() should be performed on patched dict.
                Defaults to True. If False is passed, it is convenient to not
                accept returned dict since it is the same as passed one to
                patch.

        Returns:
            Patched dictionary.
        """
        validation.validate(to_be_patched, dict)
        validation.validate(source, dict)

        patched: dictpp

        # Cast to dictpp to operation with locations. At return it's important
        # to cast it back to normal dict.
        patched = dictpp(
            deepcopy(to_be_patched) if should_deepcopy else to_be_patched,
        )

        diff = dictdiffer.diff(to_be_patched, source)

        event_name: str
        location: str
        change: Any

        for event in diff:
            # Unpack event tuple
            event_name, location, change = event
            # How dictdiffer event_name, location and change would like for a
            # reference:
            #   change BurgerShot.menu.cola (1.5, 1.8)
            #   add BurgerShot.menu [('pizza', 4.1), ('fried_chicken', 3.5)]

            # Consider only adding and changing events
            if event_name == "add":
                final_location: str
                for addition in change:
                    # Calculate final location in patched dict
                    final_location = ".".join(
                        [location, addition[0]],
                    ) if location else addition[0]
                    patched[final_location] = addition[1]

            elif event_name == "change":
                if location == "":
                    raise EmptyInputError(
                        "on change event location",
                    )
                patched[location] = change[1]

        # Cast back to normal dictionary
        return dict(patched)

    @staticmethod
    def find_location_by_field(field: Any, mp: dict) -> str:
        """
        Searches given dictionary to find given field.

        Args:
            field:
                Field value to search.
            mp:
                Dictionary to search in. All keys should be parseable to str.

        Returns:
            Location of field in form "key1.key2.key3" relative to dictionary
            root.

        Raises:
            FieldNotFoundError:
                No key with given field found in map.
        """
        key_chain: list[str] = []

        is_found: bool = MapUtils._traverse_comparing_field_location(
            field, mp, key_chain,
        )

        if not is_found:
            raise NotFoundError(
                title=f"key with field {field} in given map {mp}",
            )

        key_chain.reverse()
        return ".".join(key_chain)

    @staticmethod
    def find_field_by_location(location: str, mp: dict) -> Any:
        """Searches given map to find location and extract field.

        Args:
            location:
                What search for.
            mp:
                What to search in.

        Returns:
            Field value found.
        """
        result: Any = mp
        keys: list[str] = MapUtils._get_location_keys(location)
        keys.reverse()

        while keys:
            popped_key: str = keys.pop()
            if popped_key not in result:
                raise NotFoundError(
                    f"field for location \"{location}\" in map {mp}",
                )
            result = result[popped_key]

        return result

    @staticmethod
    def _get_location_keys(location: str) -> list[str]:
        if location == "":
            raise ValueError("empty location given")

        keys: list[str] = location.split(".")

        if keys == []:
            raise ValueError(
                f"malformed location {location}",
            )

        return keys

    @staticmethod
    def _traverse_comparing_field_location(
        field: Any,
        mp: dict,
        key_chain: list[str],
    ) -> bool:
        # Returns flag signifies whether a key was appended.

        for k, v in mp.items():
            if (
                (
                    isinstance(v, dict)
                    and MapUtils._traverse_comparing_field_location(
                        field, v, key_chain,
                    )
                )
                or v == field
            ):
                key_chain.append(str(k))
                return True

        return False
