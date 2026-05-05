# src/core/state/entity_store.py
# GROUP: core.state
# DESCRIPTION: In-memory entity storage (MVP state layer, no persistence yet)

from typing import Dict, Any, Optional
from src.shared.logging import get_logger

logger = get_logger("EntityStore")


class EntityStore:
    """
    Simple in-memory storage for entities.
    This is the first step toward Knowledge Graph / Firestore replacement.
    """

    def __init__(self):
        # structure:
        # {
        #   "hero": {
        #       "Ares": {"power": 100, "lore": "..."}
        #   }
        # }
        self._store: Dict[str, Dict[str, Dict[str, Any]]] = {}

    def create(self, entity_type: str, name: str) -> Dict[str, Any]:
        logger.info(f"[STORE] create {entity_type}:{name}")

        if entity_type not in self._store:
            self._store[entity_type] = {}

        if name in self._store[entity_type]:
            logger.warning(f"[STORE] overwriting existing entity {entity_type}:{name}")

        self._store[entity_type][name] = {}

        return self._store[entity_type][name]

    def update(self, entity_type: str, name: str, field: str, value: Any) -> bool:
        logger.info(f"[STORE] update {entity_type}:{name}.{field} = {value}")

        if entity_type not in self._store:
            return False

        if name not in self._store[entity_type]:
            return False

        self._store[entity_type][name][field] = value
        return True

    def get(self, entity_type: str, name: str) -> Optional[Dict[str, Any]]:
        return self._store.get(entity_type, {}).get(name)

    def dump(self) -> Dict[str, Any]:
        return self._store