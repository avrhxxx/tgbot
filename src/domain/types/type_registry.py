# ============================================================
# FILE: src/domain/types/type_registry.py
# PURPOSE: Entity type registry
# ============================================================

class TypeRegistry:
    def __init__(self):
        self.types = set()

    def register(self, name: str):
        self.types.add(name)

    def exists(self, name: str):
        return name in self.types