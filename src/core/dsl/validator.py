# src/core/dsl/validator.py
# PURPOSE: Validate AST commands against DSL rules (SOFT MODE - Stage 1 interactive)

from src.core.dsl.grammar import SUPPORTED_COMMANDS


class DSLValidator:
    """
    Soft validator:
    - NEVER raises exceptions
    - marks invalid commands instead
    - allows pipeline to continue execution
    """

    def __init__(self, type_registry=None, field_registry=None, relation_registry=None):
        self.type_registry = type_registry
        self.field_registry = field_registry
        self.relation_registry = relation_registry

    def validate(self, commands):
        validated = []

        for cmd in commands:

            cmd._valid = True
            cmd._error = None

            # ----------------------------
            # BASIC CHECKS
            # ----------------------------
            if not getattr(cmd, "type", None):
                cmd._valid = False
                cmd._error = "Missing command type"
                validated.append(cmd)
                continue

            if cmd.type not in SUPPORTED_COMMANDS:
                cmd._valid = False
                cmd._error = f"Unsupported command: {cmd.type}"
                validated.append(cmd)
                continue

            # ----------------------------
            # DSL RULES (SOFT MODE)
            # ----------------------------

            if cmd.type == "set_field":
                field = cmd.params.get("field")
                if self.field_registry and not self.field_registry.exists(field):
                    cmd._valid = False
                    cmd._error = f"Unknown field: {field}"

            if cmd.type == "add_relation":
                relation = cmd.params.get("relation")
                if self.relation_registry and not self.relation_registry.exists(relation):
                    cmd._valid = False
                    cmd._error = f"Unknown relation: {relation}"

            validated.append(cmd)

        return validated