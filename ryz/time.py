import time

timedata = time.struct_time

def utc() -> float:
    return time.time()

def delta(d: float, f: float | None = None) -> float:
    """
    Calculates delta timestamp from "f" (or current moment) adding given delta.

    Delta is always abs, for negative support, use "delta_signed".
    """
    return abs(delta_signed(d, f))

def delta_signed(d: float, f: float | None = None) -> float:
    """
    Calculates delta timestamp from "f" (or current moment) adding given delta.
    """
    f = f if f is not None else utc()
    return f - d

def local() -> timedata:
    return time.localtime()

def fmt(f: str, td: timedata | None = None):
    return time.strftime(f, td if td is not None else time.gmtime())
