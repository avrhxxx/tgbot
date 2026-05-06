# GROUP: shared
# DESCRIPTION: Lightweight trace context system for end-to-end request tracking

import uuid
import contextvars
from typing import Optional

_trace_id_var: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    "trace_id",
    default=None
)


def generate_trace_id() -> str:
    """
    Generates unique trace identifier for request tracking.
    """
    return uuid.uuid4().hex[:12]


def set_trace_id(trace_id: str) -> None:
    """
    Sets trace_id for current execution context.
    """
    _trace_id_var.set(trace_id)


def get_trace_id() -> Optional[str]:
    """
    Retrieves current trace_id (if exists).
    """
    return _trace_id_var.get()


def ensure_trace_id() -> str:
    """
    Ensures trace_id exists in context.
    If missing, creates a new one.
    """
    current = get_trace_id()
    if current:
        return current

    new_id = generate_trace_id()
    set_trace_id(new_id)
    return new_id