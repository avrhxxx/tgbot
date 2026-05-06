# ============================================================
# FILE: src/core/state/entity_store.py
# GROUP: core.state
# LAYER: STATE LAYER (Graph Memory)
# PURPOSE: Entity storage (Stage 1 - DSL compliant entity model + relations integrated)
# ============================================================

from typing import Dict, Any, Optional


class EntityStore:
    """
    STATE LAYER (CORE)

    ROLE:
    - stores deterministic graph state
    - holds entities, fields, relations
    - NO execution logic
    - NO DSL interpretation
    - NO error handling responsibility

    ENTITY MODEL:
    {
        "id": str,
        "name": str,
        "type": Optional[str],
        "fields": Dict[str, Any],
        "relations": List[Dict[str, str]]
    }
    """

    def __init__(self):
        self.entities: Dict[str, Dict[str, Any]] = {}

    # ============================================================
    # INTERNAL HELPERS
    # ============================================================

    def _normalize(self, name: str) -> str:
        return name.strip().lower()

    # ============================================================
    # ENTITY OPERATIONS
    # ============================================================

    def create_entity(self, name: str):
        entity_id = self._normalize(name)

        if entity_id in self.entities:
            return

        self.entities[entity_id] = {
            "id": entity_id,
            "name": name,
            "type": None,
            "fields": {},
            "relations": []
        }

    def set_entity_type(self, name: str, entity_type: str):
        entity = self.get_entity(name)

        if not entity:
            return

        entity["type"] = entity_type

    # ============================================================
    # FIELD OPERATIONS
    # ============================================================

    def set_field(self, name: str, field: str, value: Any):
        entity = self.get_entity(name)

        if not entity:
            return

        entity["fields"][field] = value

    # ============================================================
    # RELATION OPERATIONS
    # ============================================================

    def add_relation(self, from_entity: str, relation_type: str, to_entity: str):
        source = self.get_entity(from_entity)

        if not source:
            return

        target = self.get_entity(to_entity)

        if not target:
            return

        source["relations"].append({
            "type": relation_type,
            "to": self._normalize(to_entity)
        })

    def remove_relation(self, from_entity: str, relation_type: str, to_entity: str):
        source = self.get_entity(from_entity)

        if not source:
            return

        source["relations"] = [
            r for r in source["relations"]
            if not (r["type"] == relation_type and r["to"] == self._normalize(to_entity))
        ]

    # ============================================================
    # READ OPERATIONS
    # ============================================================

    def get_entity(self, name: str) -> Optional[Dict[str, Any]]:
        return self.entities.get(self._normalize(name))

    def get_all_entities(self):
        return self.entities