# ============================================================
# FILE: src/semantic/meaning_engine.py
# PURPOSE: Interprets relations semantically
# ============================================================

class MeaningEngine:
    def __init__(self, mapping):
        self.mapping = mapping

    def interpret(self, relation):
        return self.mapping.get(relation, "unknown relation")