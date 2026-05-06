# src/core/graph/relation_store.py
# GROUP: core.graph
# DESCRIPTION: Stores relations between entities (in-memory placeholder)

from typing import Dict, List


class RelationStore:
    """
    Simple in-memory relation store.
    """

    def __init__(self):
        self.relations: Dict[str, List[dict]] = {}

    def add_relation(self, source: str, relation: str, target: str):
        if source not in self.relations:
            self.relations[source] = []

        self.relations[source].append({
            "relation": relation,
            "target": target
        })

    def get_relations(self, source: str):
        return self.relations.get(source, [])