# ============================================================
# FILE: src/core/state/entity_store.py
# GROUP: core.state
# LAYER: STATE LAYER (Graph Memory)
# PURPOSE: Deterministic graph storage (Stage 1 FINAL CONTRACT)
# ============================================================

from typing import Dict, Any, Optional, List
from src.shared.logging import get_logger

logger = get_logger("entity_store")


class EntityStore:

    def __init__(self):
        self.entities: Dict[str, Dict[str, Any]] = {}

    # ============================================================
    # INTERNAL
    # ============================================================

    def _normalize(self, name: str) -> str:
        return name.strip().lower()

    def _get(self, name: str) -> Optional[Dict[str, Any]]:
        return self.entities.get(self._normalize(name))

    # ============================================================
    # ENTITY OPS
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

        logger.info(f"[EntityStore] created entity={entity_id}")

    def set_entity_type(self, name: str, entity_type: str):
        entity = self._get(name)

        if not entity:
            logger.warning(f"[EntityStore] set_entity_type failed (missing entity={name})")
            return

        entity["type"] = entity_type

    # ============================================================
    # FIELD OPS
    # ============================================================

    def set_field(self, name: str, field: str, value: Any):
        entity = self._get(name)

        if not entity:
            logger.warning(f"[EntityStore] set_field ignored (missing entity={name})")
            return

        entity["fields"][field] = value

    # ============================================================
    # RELATION OPS
    # ============================================================

    def add_relation(self, from_entity: str, relation_type: str, to_entity: str):
        source = self._get(from_entity)
        target = self._get(to_entity)

        if not source or not target:
            logger.warning(
                f"[EntityStore] add_relation failed "
                f"from={from_entity} to={to_entity} type={relation_type}"
            )
            return

        source["relations"].append({
            "type": relation_type,
            "to": self._normalize(to_entity)
        })

    def remove_relation(self, from_entity: str, relation_type: str, to_entity: str):
        source = self._get(from_entity)

        if not source:
            return

        source["relations"] = [
            r for r in source["relations"]
            if not (r["type"] == relation_type and r["to"] == self._normalize(to_entity))
        ]

    # ============================================================
    # READ OPS
    # ============================================================

    def get_entity(self, name: str) -> Optional[Dict[str, Any]]:
        return self._get(name)

    def get_all_entities(self):
        return self.entities