# src/shared/logging.py
# GROUP: shared
# DESCRIPTION: Centralized logging utility with trace support

import logging

from src.shared.trace import get_trace_id


class TraceFilter(logging.Filter):
    """
    Injects trace_id into every log record
    """

    def filter(self, record: logging.LogRecord) -> bool:
        record.trace_id = get_trace_id() or "no-trace"
        return True


def get_logger(name: str) -> logging.Logger:
    """
    Returns standardized logger instance
    used across CORE + INFRA + AI layers
    """

    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "[%(asctime)s] [trace=%(trace_id)s] [%(levelname)s] [%(name)s] %(message)s"
        )

        handler.setFormatter(formatter)

        # 🔥 TRACE INJECTION
        logger.addFilter(TraceFilter())

        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger