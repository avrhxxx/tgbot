# src/config/base.py
# GROUP: config.base
# DESCRIPTION: Safe environment loader (strict + production-safe fail-fast)

import os


class ImproperlyConfigured(Exception):
    """
    Raised when critical environment configuration is missing or invalid.
    """
    pass


def get_env(name: str, default=None, required: bool = True) -> str:
    """
    Safe env getter with strict validation.

    Rules:
    - required=True → must exist and be non-empty
    - required=False → fallback allowed
    - trims whitespace to avoid silent misconfigurations
    """

    value = os.getenv(name, default)

    # normalize
    if isinstance(value, str):
        value = value.strip()

    # fail-fast validation
    if required:
        if value is None or value == "":
            raise ImproperlyConfigured(f"Missing or empty env var: {name}")

    return value