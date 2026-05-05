# src/core/state/state_manager.py
# GROUP: core.state
# DESCRIPTION: Single entrypoint for state mutations (abstraction layer for future DB/Graph)

from src.core.state.entity_store import EntityStore
from src.shared.logging import get_logger

logger = get_logger("StateManager")


class StateManager:
    """
    Facade over EntityStore.
    In future: will route to Firestore / Graph DB / hybrid storage.
    """

    def __init__(self):
        self.store = EntityStore()

    def create(self, entity_type: str, name: str):
        logger.info(f"[STATE] create {entity_type}:{name}")
        return self.store.create(entity_type, name)

    def update(self, entity_type: str, name: str, field: str, value):
        logger.info(f"[STATE] update {entity_type}:{name}.{field}={value}")
        return self.store.update(entity_type, name, field, value)

    def get(self, entity_type: str, name: str):
        return self.store.get(entity_type, name)

    def dump(self):
        return self.store.dump()