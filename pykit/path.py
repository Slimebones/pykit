import os
from pathlib import Path

from pykit.cls import Static


class PathUtils(Static):
    @staticmethod
    def get_script_path(filedunder: str) -> Path:
        """
        Retrieves the path to the script.

        Args:
            filedunder:
                __file__ dunder taking from the target script.
        """
        return Path(os.path.realpath(filedunder))

    @staticmethod
    def get_script_dir(filedunder: str) -> Path:
        """
        Retrieves the path to the script's dir.

        Args:
            filedunder:
                __file__ dunder taking from the target script.
        """
        return PathUtils.get_script_path(filedunder).parent
