# src/core/state/state_manager.py
# GROUP: core.state
# DESCRIPTION: Single entrypoint for state mutations (contract-safe facade layer)

from typing import Any, Optional, Dict

from src.core.state.entity_store import EntityStore
from src.shared.logging import get_logger

logger = get_logger("StateManager")


class StateManager:
    """
    Facade over EntityStore.

    Guarantees:
    - stable return contracts
    - safe mutation layer
    - future DB/Graph abstraction point
    """

    def __init__(self):
        self.store = EntityStore()

    def create(self, entity_type: str, name: str) -> Dict[str, Any]:
        logger.info(f"[STATE] create {entity_type}:{name}")

        result = self.store.create(entity_type, name)

        return {
            "ok": True,
            "action": "create",
            "entity_type": entity_type,
            "name": name,
            "result": result
        }

    def update(
        self,
        entity_type: str,
        name: str,
        field: str,
        value: Any
    ) -> Dict[str, Any]:
        logger.info(f"[STATE] update {entity_type}:{name}.{field}={value}")

        if not field:
            return {
                "ok": False,
                "error": "missing_field"
            }

        result = self.store.update(entity_type, name, field, value)

        if result is False:
            return {
                "ok": False,
                "error": "not_found",
                "entity_type": entity_type,
                "name": name
            }

        return {
            "ok": True,
            "action": "update",
            "entity_type": entity_type,
            "name": name,
            "field": field,
            "value": value,
            "result": result
        }

    def get(self, entity_type: str, name: str) -> Optional[Dict[str, Any]]:
        return self.store.get(entity_type, name)

    def dump(self) -> Dict[str, Any]:
        return self.store.dump()