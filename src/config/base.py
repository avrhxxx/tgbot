# src/config/base.py
# =========================================
# GROUP: config
# FILE: base.py
# DESCRIPTION:
# Base config helpers for environment variables loading.
# Provides strict getenv with validation for required ENV vars.
# =========================================

import os


class ImproperlyConfigured(Exception):
    def __init__(self, variable_name: str):
        self.variable_name = variable_name
        self.message = f"Set the {variable_name} environment variable."
        super().__init__(self.message)


def getenv(var_name: str, cast_to=str):
    try:
        value = os.environ[var_name]
        return cast_to(value)

    except KeyError as err:
        raise ImproperlyConfigured(var_name) from err

    except ValueError as err:
        raise ValueError(f"Cannot cast {var_name} to {cast_to}") from err