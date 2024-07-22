import asyncio
import sys
from multiprocessing import Pipe, Process
from typing import Any, Literal, Protocol
from xml.dom import NotFoundErr

from pykit.err import ValErr
from pykit.log import log
from pykit.res import Err, Ok, Res

if sys.platform == "win32":
    from multiprocessing.connection import PipeConnection as PipeConn
else:
    from multiprocessing.connection import Connection as PipeConn


class ProcTarget(Protocol):
    def __call__(self, **kwargs: Any) -> Any: ...

class ProcGroup:
    """
    Organizes processes.

    By default, processes are using Pipes to communicate.

    Args:
        max_procs:
            Maximum processes to handle. Defaults to -1, which is unlimited.
    """

    def __init__(self, max_procs: int = -1) -> None:
        self._procs: dict[int, tuple[Process, PipeConn]] = {}
        self._key_to_pid: dict[str, int] = {}
        self._max_procs = max_procs
        self.proc_dereg_method: Literal["kill", "terminate"] = "terminate"

    def has(self, pid: int) -> bool:
        return pid in self._procs

    def has_key(self, key: str) -> bool:
        return key in self._key_to_pid

    def _can_reg_by_limit(self) -> bool:
        return \
            self._max_procs < 0 or (len(self._procs) + 1 <= self._max_procs)

    def reg(
            self,
            target: ProcTarget,
            key: str | None = None,
            *,
            proc_kwargs: dict[str, Any] | None = None) -> Res[int]:
        """
        Regs a new process.

        Process's target can only accept kwargs, args are reserved for
        interfacing uses.
        """
        if not self._can_reg_by_limit():
            return Err(ValErr(
                "cannot reg a new process:"
                f" limit {self._max_procs} is exceeded"))

        parent_pipe, child_pipe = Pipe()
        proc = Process(
            target=target,
            args=(child_pipe,),
            kwargs=proc_kwargs if proc_kwargs else {})
        proc.start()

        if proc.pid is None:
            return Err(SystemError(
                f"proc {proc} has been started, but the pid is unassigned"))
        if self.has(proc.pid):
            proc.kill()
            return Err(ValErr(
                "new process is started with the same pid as regd"
                " one => kill new process"))

        if key:
            if key in self._key_to_pid:
                return Err(ValErr(f"key {key} is already regd"))
            self._key_to_pid[key] = proc.pid

        self._procs[proc.pid] = (proc, parent_pipe)
        return Ok(proc.pid)

    def get_pid_by_key(self, key: str) -> Res[int]:
        if key not in self._key_to_pid:
            return Err(NotFoundErr(f"key {key}"))
        return Ok(self._key_to_pid[key])

    def try_dereg_key(self, key: str) -> Res[bool]:
        pid_res = self.get_pid_by_key(key)
        if isinstance(pid_res, Err):
            return pid_res
        return self.try_dereg(pid_res.unwrap())

    def _end_proc(self, proc: Process):
        if self.proc_dereg_method == "kill":
            proc.kill()
        elif self.proc_dereg_method == "terminate":
            proc.terminate()
        else:
            log.err(
                f"unrecoznized {self.proc_dereg_method}"
                " => use \"terminate\"")

    def try_dereg(self, pid: int) -> Res[bool]:
        """
        Deregs a process by pid.

        The process is killed if it's still alive.
        """
        if pid not in self._procs:
            return Ok(False)

        proc, _ = self._procs[pid]
        if proc.is_alive():
            self._end_proc(proc)

        for key, map_pid in self._key_to_pid.items():
            if map_pid == pid:
                del self._key_to_pid[key]
                break

        del self._procs[pid]
        return Ok(True)

    def recv(self, pid: int) -> Res[Any]:
        proc_data = self._get_proc(pid)
        if isinstance(proc_data, Err):
            return proc_data
        _, pipe = self._get_proc(pid).unwrap()
        data = pipe.recv()
        return Ok(data)

    def recv_key(self, key: str) -> Res[Any]:
        pid_res = self.get_pid_by_key(key)
        if isinstance(pid_res, Err):
            return pid_res
        return self.recv(pid_res.unwrap())

    async def async_recv_key(self, key: str, period: float = 1.0) -> Res[Any]:
        pid_res = self.get_pid_by_key(key)
        if isinstance(pid_res, Err):
            return pid_res
        return await self.async_recv(pid_res.unwrap(), period)

    async def async_recv(self, pid: int, period: float = 1.0) -> Res[Any]:
        """
        Same as recv(), but async.

        Due to problems with implementing this both for Linux and Windows,
        a simple periodic pipe.poll() + pipe.recv() is used. Due to that,
        providing the "period" var is required.
        """
        _, pipe = self._get_proc(pid).unwrap()
        while True:
            if pipe.poll():
                return Ok(pipe.recv())
            await asyncio.sleep(period)

    def send(self, pid: int, data: Any) -> Res[None]:
        proc_data = self._get_proc(pid)
        if isinstance(proc_data, Err):
            return proc_data
        proc_res = self._get_proc(pid)
        if isinstance(proc_res, Err):
            return proc_res
        _, pipe = proc_res.unwrap()
        pipe.send(data)
        return Ok(None)

    def send_key(self, key: str, data: Any) -> Res[None]:
        pid_res = self.get_pid_by_key(key)
        if isinstance(pid_res, Err):
            return pid_res
        pid = pid_res.unwrap()
        return self.send(pid, data)

    def _get_proc(self, pid: int) -> Res[tuple[Process, PipeConn]]:
        if not self.has(pid):
            return Err(NotFoundErr(f"proc with pid {pid}"))
        proc, pipe = self._procs[pid]
        if not proc.is_alive():
            self.try_dereg(pid).unwrap()
            return Err(ValErr("process is closed"))
        return Ok((proc, pipe))
