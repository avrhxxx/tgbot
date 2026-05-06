# src/core/dsl/validator.py
# GROUP: core.dsl
# DESCRIPTION: DSL validator (Stage 1 - structural validation only, NON-BLOCKING)

from src.core.dsl.grammar import SUPPORTED_COMMANDS


class DSLValidator:
    """
    Stage 1 Validator (FINAL BEHAVIOR)

    ROLE:
    - structural check only
    - diagnostic layer (NOT a gate)
    - never blocks execution
    - never raises exceptions
    """

    def __init__(self, type_registry=None, field_registry=None, relation_registry=None):
        self.type_registry = type_registry
        self.field_registry = field_registry
        self.relation_registry = relation_registry

    def validate(self, commands):
        """
        Returns:
            List[CommandNode] (unchanged, annotated optionally in future)
        """

        for cmd in commands:

            # =========================
            # BASIC SAFETY CHECK
            # =========================
            if not getattr(cmd, "type", None):
                cmd._valid = False
                cmd._error = "Missing command type"
                continue

            # =========================
            # REGISTRY CHECK (SOFT)
            # =========================
            if cmd.type not in SUPPORTED_COMMANDS:
                cmd._valid = False
                cmd._error = f"Unsupported command: {cmd.type}"
                continue

            # =========================
            # VALID COMMAND MARK
            # =========================
            cmd._valid = True
            cmd._error = None

        return commands