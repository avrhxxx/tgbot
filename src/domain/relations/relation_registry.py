# ============================================================
# FILE: src/domain/relations/relation_registry.py
# PURPOSE: Relation registry
# ============================================================

class RelationRegistry:
    def __init__(self):
        self.relations = set()

    def register(self, name: str):
        self.relations.add(name)

    def exists(self, name: str):
        return name in self.relations