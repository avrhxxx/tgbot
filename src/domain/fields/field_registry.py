# ============================================================
# FILE: src/domain/fields/field_registry.py
# PURPOSE: Field registry
# ============================================================

class FieldRegistry:
    def __init__(self):
        self.fields = set()

    def register(self, name: str):
        self.fields.add(name)

    def exists(self, name: str):
        return name in self.fields