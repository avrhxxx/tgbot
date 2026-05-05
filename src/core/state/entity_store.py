# src/core/state/entity_store.py
# GROUP: core.state
# DESCRIPTION: In-memory entity storage (MVP state layer, contract-stable)

from typing import Dict, Any, Optional
from src.shared.logging import get_logger

logger = get_logger("EntityStore")


class EntityStore:
    """
    Simple in-memory storage for entities.

    Design goal:
    - deterministic behavior
    - predictable return values
    - future replacement with Graph DB / Firestore
    """

    def __init__(self):
        self._store: Dict[str, Dict[str, Dict[str, Any]]] = {}

    def create(self, entity_type: str, name: str) -> Dict[str, Any]:
        logger.info(f"[STORE] create {entity_type}:{name}")

        if entity_type not in self._store:
            self._store[entity_type] = {}

        existed = name in self._store[entity_type]

        self._store[entity_type][name] = {}

        return {
            "created": True,
            "overwritten": existed,
            "entity_type": entity_type,
            "name": name
        }

    def update(self, entity_type: str, name: str, field: str, value: Any) -> Dict[str, Any]:
        logger.info(f"[STORE] update {entity_type}:{name}.{field} = {value}")

        if entity_type not in self._store:
            return {
                "ok": False,
                "error": "entity_type_not_found"
            }

        if name not in self._store[entity_type]:
            return {
                "ok": False,
                "error": "entity_not_found"
            }

        self._store[entity_type][name][field] = value

        return {
            "ok": True,
            "entity_type": entity_type,
            "name": name,
            "field": field,
            "value": value
        }

    def get(self, entity_type: str, name: str) -> Optional[Dict[str, Any]]:
        return self._store.get(entity_type, {}).get(name)

    def dump(self) -> Dict[str, Any]:
        return self._store