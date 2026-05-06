# src/core/dsl/validator.py
# GROUP: core.dsl
# DESCRIPTION: DSL validator (Stage 1 - structural validation only)

from src.core.dsl.errors import DSLValidationError
from src.core.dsl.grammar import SUPPORTED_COMMANDS


class DSLValidator:
    """
    Stage 1 Validator

    ROLE:
    - verifies DSL structure
    - ensures command type exists in registry
    - DOES NOT block bootstrap operations
    - DOES NOT modify AST
    """

    def __init__(self, type_registry=None, field_registry=None, relation_registry=None):
        self.type_registry = type_registry
        self.field_registry = field_registry
        self.relation_registry = relation_registry

    def validate(self, commands):
        """
        Returns:
            commands (unchanged AST list)
        """

        for cmd in commands:

            # -----------------------------
            # BASIC STRUCTURE CHECK
            # -----------------------------
            if not getattr(cmd, "type", None):
                raise DSLValidationError("Missing command type")

            if cmd.type not in SUPPORTED_COMMANDS:
                raise DSLValidationError(f"Unsupported command: {cmd.type}")

            # -----------------------------
            # STAGE 1 BOOTSTRAP POLICY
            # -----------------------------
            # Validator is intentionally NON-BLOCKING for:
            # - create_field
            # - create_type
            # - create_relation
            # - set_field
            # - add_relation

            # Future Stage 2: registry enforcement will be activated here

        return commands