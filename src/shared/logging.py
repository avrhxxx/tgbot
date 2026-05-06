# GROUP: shared
# DESCRIPTION: Centralized logging utility with trace support (Stage 1 improved observability)

import logging

from src.shared.trace import get_trace_id, ensure_trace_id


class TraceFilter(logging.Filter):
    """
    Injects trace_id into every log record
    """

    def filter(self, record: logging.LogRecord) -> bool:
        record.trace_id = get_trace_id() or "no-trace"
        return True


class StageFormatter(logging.Formatter):
    """
    Adds lightweight visual structure for pipeline debugging
    without breaking standard logging system
    """

    def format(self, record: logging.LogRecord) -> str:
        base = super().format(record)

        # lightweight visual grouping hints
        msg = record.getMessage()

        if "PIPELINE START" in msg:
            return f"\n==== {base} ===="
        if "PIPELINE END" in msg:
            return f"==== {base} ====\n"

        return base


def get_logger(name: str) -> logging.Logger:
    """
    Returns standardized logger instance
    used across CORE + INFRA + AI layers
    """

    ensure_trace_id()

    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()

        handler.addFilter(TraceFilter())

        formatter = StageFormatter(
            "[%(asctime)s] [trace=%(trace_id)s] [%(levelname)s] [%(name)s] %(message)s"
        )

        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger