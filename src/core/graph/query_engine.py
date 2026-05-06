# src/core/graph/query_engine.py
# GROUP: core.graph
# DESCRIPTION: Query layer over graph (placeholder)

from src.core.graph.relation_store import RelationStore


class QueryEngine:
    """
    Provides read access to graph.
    """

    def __init__(self, relation_store: RelationStore):
        self.relation_store = relation_store

    def get_relations(self, entity: str):
        return self.relation_store.get_relations(entity)