import subprocess
from typing import Callable

from pykit.log import log


class SubprocUtils:
    @classmethod
    def popen(
        cls,
        cmd: str,
        fn: Callable[[subprocess.Popen], None],
        *,
        must_raise_retcode_err: bool = True,
    ):
        """
        Creates popen and calls given fn with it.

        Fn to read stdout example:
        ```python
        def myfn(proc):
            if proc.stdout:
                for line in proc.stdout:
                    print(line, end="")  # do whatever you want
        ```
        """
        with subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            text=True,
            shell=True,  # noqa: S602
        ) as process:
            try:
                fn(process)
            except KeyboardInterrupt:
                log.info("receive keyboard interrupt => kill subproc")
                process.kill()
                raise
        if must_raise_retcode_err and process.returncode != 0:
            raise subprocess.CalledProcessError(
                process.returncode,
                process.args,
            )

