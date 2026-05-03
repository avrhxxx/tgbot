# src/config/base.py
# GROUP: config
# DESCRIPTION: SAFE environment loader (Railway-friendly)

import os


class ImproperlyConfigured(Exception):
    pass


def getenv(var_name: str, cast_to=str, default=None, required: bool = True):
    value = os.getenv(var_name, default)

    if value is None:
        if required:
            raise ImproperlyConfigured(f"Missing env: {var_name}")
        return default

    try:
        return cast_to(value)
    except Exception as err:
        raise ValueError(f"Cannot cast env {var_name}") from err