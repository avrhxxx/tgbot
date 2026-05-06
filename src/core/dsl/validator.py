# src/core/dsl/validator.py
# PURPOSE: Validate AST commands against DSL rules

from src.core.dsl.errors import DSLValidationError
from src.core.dsl.grammar import SUPPORTED_COMMANDS


class DSLValidator:
    """
    Validates parsed AST commands.
    """

    def validate(self, commands):
        for cmd in commands:

            # TYPE MUST EXIST
            if not getattr(cmd, "type", None):
                raise DSLValidationError("Missing command type")

            # TYPE MUST BE REGISTERED
            if cmd.type not in SUPPORTED_COMMANDS:
                raise DSLValidationError(f"Unsupported command: {cmd.type}")

        return True