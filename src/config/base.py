# src/config/base.py
# GROUP: config.base
# DESCRIPTION: Safe environment loader (strict + fail-fast)

import os


class ImproperlyConfigured(Exception):
    pass


def get_env(name: str, default=None, required: bool = True) -> str:
    """
    Safe env getter:
    - required=True → crash if missing
    - required=False → fallback allowed
    """
    value = os.getenv(name, default)

    if required and not value:
        raise ImproperlyConfigured(f"Missing env var: {name}")

    return value