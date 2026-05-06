# GROUP: shared
# DESCRIPTION: Centralized logging utility with trace support (Stage 1 Observability v3 - mobile readable FIXED)

import logging
import time
import textwrap
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
# FORMATTER (SAFE WRAP - FIXED)
# =========================================

class StageFormatter(logging.Formatter):
    MAX_WIDTH = 90  # 🔥 lepsze pod mobile (100 często za szerokie)

    def format(self, record: logging.LogRecord) -> str:
        original_msg = record.getMessage()

        wrapped_msg = self._wrap_message(original_msg)

        # 🔥 NIE robimy replace() — tylko podmieniamy message bezpośrednio
        record.message = wrapped_msg

        base = super().format(record)

        if "PIPELINE START" in original_msg:
            return f"\n==== {base} ===="
        if "PIPELINE END" in original_msg:
            return f"==== {base} ====\n"

        return base

    def _wrap_message(self, msg: str) -> str:
        if "\n" not in msg and len(msg) < self.MAX_WIDTH:
            return msg

        lines = msg.split("\n")
        wrapped_lines = []

        for line in lines:
            if not line.strip():
                wrapped_lines.append("")
                continue

            stripped = line.lstrip()
            indent_size = len(line) - len(stripped)

            wrapped = textwrap.fill(
                stripped,
                width=self.MAX_WIDTH,
                subsequent_indent=" " * indent_size,
                break_long_words=False,
                break_on_hyphens=False
            )

            # zachowanie indentu
            wrapped_lines.append(wrapped)

        return "\n".join(wrapped_lines)


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
        logger.propagate = False  # 🔥 ważne: brak duplikacji logów

    return logger


# =========================================
# STAGE HELPERS
# =========================================

def log_stage_start(logger: logging.Logger, name: str):
    logger.info(f"▶ {name}")


def log_stage_success(logger: logging.Logger, duration_ms: float):
    logger.info(f"✔ OK ({duration_ms:.2f}ms)")


def log_stage_error(logger: logging.Logger, duration_ms: float):
    logger.error(f"✖ ERROR ({duration_ms:.2f}ms)")


def log_action(logger: logging.Logger, action: str, detail: str = ""):
    if detail:
        logger.info(f"↳ {action} | {detail}")
    else:
        logger.info(f"↳ {action}")


# =========================================
# TIMER CONTEXT
# =========================================

@contextmanager
def timed_stage(logger: logging.Logger, name: str):
    log_stage_start(logger, name)
    start = time.time()

    try:
        yield
        duration = (time.time() - start) * 1000
        log_stage_success(logger, duration)
    except Exception:
        duration = (time.time() - start) * 1000
        log_stage_error(logger, duration)
        raise