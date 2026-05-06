# ============================================================
# FILE: src/domain/schema_validator.py
# PURPOSE: Validate graph schema usage
# ============================================================

class SchemaValidator:
    def __init__(self, type_registry, field_registry, relation_registry):
        self.type_registry = type_registry
        self.field_registry = field_registry
        self.relation_registry = relation_registry

    def validate(self, command):
        # placeholder (Stage 1 minimal)
        return True