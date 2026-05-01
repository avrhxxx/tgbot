# src/config/base.py
# GROUP: config
# DESCRIPTION: Strict environment loader

import os


class ImproperlyConfigured(Exception):
    def __init__(self, variable_name: str):
        super().__init__(f"Set the {variable_name} environment variable.")


def getenv(var_name: str, cast_to=str, default=None):
    value = os.getenv(var_name, default)

    if value is None:
        raise ImproperlyConfigured(var_name)

    try:
        return cast_to(value)
    except Exception as err:
        raise ValueError(f"Cannot cast {var_name}") from err