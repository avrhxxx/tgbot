# src/core/state/entity_store.py
# GROUP: core.state
# DESCRIPTION: Entity storage (Stage 1 - DSL compliant entity model)

from typing import Dict, Any, Optional


class EntityStore:
    """
    Stores entities in DSL-compliant structure.

    ENTITY MODEL:
    {
        "id": str,
        "name": str,
        "type": Optional[str],
        "fields": Dict[str, Any]
    }
    """

    def __init__(self):
        self.entities: Dict[str, Dict[str, Any]] = {}

    # -----------------------------
    # INTERNAL
    # -----------------------------

    def _normalize(self, name: str) -> str:
        return name.strip().lower()

    # -----------------------------
    # ENTITY OPS
    # -----------------------------

    def create_entity(self, name: str):
        entity_id = self._normalize(name)

        if entity_id in self.entities:
            return

        self.entities[entity_id] = {
            "id": entity_id,
            "name": name,
            "type": None,
            "fields": {}
        }

    def set_entity_type(self, name: str, entity_type: str):
        entity = self.get_entity(name)

        if not entity:
            raise ValueError(f"Entity not found: {name}")

        entity["type"] = entity_type

    # -----------------------------
    # FIELD OPS
    # -----------------------------

    def set_field(self, name: str, field: str, value: Any):
        entity = self.get_entity(name)

        if not entity:
            self.create_entity(name)
            entity = self.get_entity(name)

        entity["fields"][field] = value

    # -----------------------------
    # READ OPS
    # -----------------------------

    def get_entity(self, name: str) -> Optional[Dict[str, Any]]:
        entity_id = self._normalize(name)
        return self.entities.get(entity_id)

    def get_all_entities(self):
        return self.entities