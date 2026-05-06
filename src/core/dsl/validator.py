from src.core.dsl.errors import DSLValidationError
from src.core.dsl.grammar import SUPPORTED_COMMANDS


class DSLValidator:

    def __init__(self, type_registry=None, field_registry=None, relation_registry=None):
        self.type_registry = type_registry
        self.field_registry = field_registry
        self.relation_registry = relation_registry

    def validate(self, commands):

        for cmd in commands:

            if not getattr(cmd, "type", None):
                raise DSLValidationError("Missing command type")

            if cmd.type not in SUPPORTED_COMMANDS:
                raise DSLValidationError(f"Unsupported command: {cmd.type}")

            # ============================
            # STAGE 1 BOOT MODE (IMPORTANT)
            # ============================

            # ❗ NIE BLOKUJEMY FIELD/TYPE/RELATION
            # bo system musi sam się zbootstrapować

            if cmd.type == "set_field":
                continue

            if cmd.type in {"add_relation"}:
                continue

        return True