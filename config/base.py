# config/base.py
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
    except KeyError:
        raise ImproperlyConfigured(var_name)
    except ValueError:
        raise ValueError(f"Cannot cast {var_name} to {cast_to}")