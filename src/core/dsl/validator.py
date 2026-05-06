# src/core/dsl/validator.py
# PURPOSE: Validate AST commands against DSL rules

from src.core.dsl.errors import DSLValidationError
from src.core.dsl.grammar import SUPPORTED_COMMANDS


class DSLValidator:
    """
    Validates parsed AST commands.
    """

    def __init__(self, type_registry=None, field_registry=None, relation_registry=None):
        self.type_registry = type_registry
        self.field_registry = field_registry
        self.relation_registry = relation_registry

    def validate(self, commands):
        for cmd in commands:

            # ----------------------------
            # BASIC STRUCTURE CHECK
            # ----------------------------
            if not getattr(cmd, "type", None):
                raise DSLValidationError("Missing command type")

            if cmd.type not in SUPPORTED_COMMANDS:
                raise DSLValidationError(f"Unsupported command: {cmd.type}")

            # ----------------------------
            # STRICT DSL RULES (Stage 1 in-memory mode)
            # ----------------------------

            if cmd.type == "set_field":
                if self.field_registry and not self.field_registry.exists(cmd.params["field"]):
                    raise DSLValidationError(f"Unknown field: {cmd.params['field']}")

            if cmd.type in {"add_relation"}:
                if self.relation_registry and not self.relation_registry.exists(cmd.params["relation"]):
                    raise DSLValidationError(f"Unknown relation: {cmd.params['relation']}")

        return True