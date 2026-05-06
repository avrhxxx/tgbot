# ============================================================
# FILE: src/core/dsl/validator.py
# PURPOSE: Validate AST commands against DSL rules
# ============================================================

from src.core.dsl.errors import DSLValidationError


class DSLValidator:
    """
    Validates parsed AST commands.
    """

    def validate(self, commands):
        for cmd in commands:
            if not cmd.type:
                raise DSLValidationError("Missing command type")

        return True