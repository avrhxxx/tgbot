# ============================================================
# FILE: src/semantic/interpretation.py
# PURPOSE: High-level semantic interpretation
# ============================================================

class Interpreter:
    def __init__(self, meaning_engine):
        self.meaning_engine = meaning_engine

    def describe_relation(self, relation):
        return self.meaning_engine.interpret(relation)