# GROUP: core.graph
# DESCRIPTION: Unified read layer for AI + API (Stage 1 World Query API)

from typing import Dict, List, Any, Optional
from src.core.state.entity_store import EntityStore
from src.core.graph.relation_store import RelationStore


class WorldQueryAPI:
    """
    Single read interface for entire knowledge graph.
    AI, Telegram, and future services MUST use this.
    """

    def __init__(self, entity_store: EntityStore, relation_store: RelationStore):
        self.entity_store = entity_store
        self.relation_store = relation_store

    # =========================================
    # ENTITY ACCESS
    # =========================================

    def get_entity(self, entity_id: str) -> Optional[Dict[str, Any]]:
        entity = self.entity_store.get(entity_id)
        if not entity:
            return None

        return {
            "id": entity_id,
            "type": getattr(entity, "type", None),
            "fields": getattr(entity, "fields", {}),
        }

    # =========================================
    # FULL CONTEXT (AI MAIN ENTRYPOINT)
    # =========================================

    def get_full_context(self, entity_id: str) -> Dict[str, Any]:
        entity = self.get_entity(entity_id)

        if not entity:
            return {
                "status": "not_found",
                "entity_id": entity_id,
                "relations": [],
                "related": []
            }

        relations = self.relation_store.get_by_source(entity_id) or []

        return {
            "status": "ok",
            "entity": entity,
            "relations": relations,
            "related_entities": self._collect_related_entities(relations)
        }

    # =========================================
    # SEARCH (KEYWORD LAYER v1)
    # =========================================

    def search_entities(self, keyword: str) -> List[Dict[str, Any]]:
        results = []

        for entity_id, entity in self.entity_store.all().items():
            if keyword.lower() in entity_id.lower():
                results.append({
                    "id": entity_id,
                    "type": getattr(entity, "type", None)
                })

        return results

    # =========================================
    # RELATION TRAVERSAL
    # =========================================

    def traverse_relations(self, entity_id: str, depth: int = 1) -> Dict[str, Any]:
        visited = set()
        output = {}

        def walk(current, level):
            if level > depth or current in visited:
                return

            visited.add(current)

            relations = self.relation_store.get_by_source(current) or []
            output[current] = relations

            for rel in relations:
                target = rel.get("to")
                if target:
                    walk(target, level + 1)

        walk(entity_id, 0)

        return output

    # =========================================
    # INTERNAL
    # =========================================

    def _collect_related_entities(self, relations: List[Dict]) -> List[str]:
        return list({r.get("to") for r in relations if r.get("to")})