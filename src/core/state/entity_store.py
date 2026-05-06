# src/core/state/entity_store.py
# GROUP: core.state
# DESCRIPTION: Entity storage (in-memory placeholder)

from typing import Dict, Any


class EntityStore:
    """
    Stores entities and their fields.
    """

    def __init__(self):
        self.entities: Dict[str, Dict[str, Any]] = {}

    def create_entity(self, name: str):
        if name not in self.entities:
            self.entities[name] = {}

    def set_field(self, name: str, field: str, value: Any):
        if name not in self.entities:
            self.create_entity(name)

        self.entities[name][field] = value

    def get_entity(self, name: str):
        return self.entities.get(name)