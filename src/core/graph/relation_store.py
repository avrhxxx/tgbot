# src/core/graph/relation_store.py
# GROUP: core.graph
# DESCRIPTION: Stores relations between entities (in-memory placeholder)

from typing import Dict, List, Optional


class RelationStore:
    """
    Simple in-memory relation store.
    """

    def __init__(self):
        self.relations: Dict[str, List[dict]] = {}

    # ============================================================
    # WRITE OPS
    # ============================================================

    def add_relation(self, source: str, relation: str, target: str):
        if source not in self.relations:
            self.relations[source] = []

        self.relations[source].append({
            "relation": relation,
            "target": target
        })

    # ============================================================
    # CORE QUERY ENGINE API (FIX FOR MYPI / QUERY ENGINE)
    # ============================================================

    def get_by_source(self, source: str) -> List[dict]:
        return self.relations.get(source, [])

    # (optional future-proofing for graph traversal)
    def get_by_target(self, target: str) -> List[dict]:
        result = []
        for src, rels in self.relations.items():
            for r in rels:
                if r.get("target") == target:
                    result.append({
                        "source": src,
                        **r
                    })
        return result

    # ============================================================
    # LEGACY COMPATIBILITY
    # ============================================================

    def get_relations(self, source: str):
        return self.relations.get(source, [])