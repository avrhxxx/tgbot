# GROUP: shared
# DESCRIPTION: Centralized logging utility with trace support (Stage 1 Observability v2)

import logging
import time
from contextlib import contextmanager

from src.shared.trace import get_trace_id, ensure_trace_id


# =========================================
# TRACE FILTER
# =========================================

class TraceFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.trace_id = get_trace_id() or "no-trace"
        return True


# =========================================
# FORMATTER
# =========================================

class StageFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        base = super().format(record)
        msg = record.getMessage()

        if "PIPELINE START" in msg:
            return f"\n==== {base} ===="
        if "PIPELINE END" in msg:
            return f"==== {base} ====\n"

        return base


# =========================================
# LOGGER FACTORY
# =========================================

def get_logger(name: str) -> logging.Logger:
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


# =========================================
# STAGE HELPERS
# =========================================

def log_stage_start(logger: logging.Logger, name: str):
    logger.info(f"  ▶ {name}")


def log_stage_success(logger: logging.Logger, duration_ms: int):
    logger.info(f"    ✔ OK ({duration_ms}ms)")


def log_stage_error(logger: logging.Logger, duration_ms: int):
    logger.error(f"    ✖ ERROR ({duration_ms}ms)")


def log_action(logger: logging.Logger, action: str, detail: str = ""):
    if detail:
        logger.info(f"    ↳ {action} ({detail})")
    else:
        logger.info(f"    ↳ {action}")


# =========================================
# TIMER CONTEXT
# =========================================

@contextmanager
def timed_stage(logger: logging.Logger, name: str):
    log_stage_start(logger, name)
    start = time.time()

    try:
        yield
        duration = int((time.time() - start) * 1000)
        log_stage_success(logger, duration)
    except Exception:
        duration = int((time.time() - start) * 1000)
        log_stage_error(logger, duration)
        raise