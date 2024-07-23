"""
Tools for working with traceback.
"""
import traceback


def fmt_stack_summary(summary: traceback.StackSummary) -> str:
    return "".join(list(traceback.StackSummary.from_list(summary).format()))

def get_traceback_str(err: Exception) -> str | None:
    s = None
    tb = err.__traceback__
    if tb:
        summary = traceback.extract_tb(tb)
        s = fmt_stack_summary(summary)
    return s
