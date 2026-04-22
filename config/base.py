import os


class ImproperlyConfigured(Exception):
    """Raises when a environment variable is missing."""

    def __init__(self, variable_name: str, *args, **kwargs):
        self.variable_name = variable_name
        self.message = f"Set the {variable_name} environment variable."
        super().__init__(self.message, *args, **kwargs)


def getenv(var_name: str, cast_to=str):
    """Gets an environment variable or raises an exception.

    Args:
        var_name: An environment variable name.
        cast_to: A type to cast.

    Returns:
        A value of the environment variable.

    Raises:
        ImproperlyConfigured: If the environment variable is missing.
    """
    try:
        value = os.environ[var_name]
        return cast_to(value)
    except KeyError:
        raise ImproperlyConfigured(var_name)
    except ValueError:
        raise ValueError(f"The value {value} can't be cast to {cast_to}.")


# =========================
# SAFE BOOL PARSER (NEW)
# =========================

def getenv_bool(var_name: str, default: bool = False) -> bool:
    """
    Safe boolean environment parser.

    Accepts:
    - "true", "1", "yes", "y", "on" → True
    - "false", "0", "no", "n", "off" → False
    """
    try:
        value = os.environ[var_name].strip().lower()
    except KeyError:
        return default

    if value in ("true", "1", "yes", "y", "on"):
        return True
    if value in ("false", "0", "no", "n", "off"):
        return False

    raise ValueError(f"Invalid boolean value for {var_name}: {value}")