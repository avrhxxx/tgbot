# src/shared/logging.py
# GROUP: shared
# DESCRIPTION: Centralized logging utility for full system traceability

import logging


def get_logger(name: str) -> logging.Logger:
    """
    Returns standardized logger instance
    used across CORE + INFRA + AI layers
    """

    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger