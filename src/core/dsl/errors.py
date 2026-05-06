# src/core/dsl/errors.py
# GROUP: core.dsl
# DESCRIPTION: DSL-specific error definitions


class DSLParseError(Exception):
    """Raised when DSL parsing fails."""
    pass


class DSLValidationError(Exception):
    """Raised when DSL validation fails."""
    pass