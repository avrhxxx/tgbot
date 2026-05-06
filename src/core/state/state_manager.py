# ============================================================
# FILE: src/core/state/state_manager.py
# PURPOSE: State coordination layer
# ============================================================

class StateManager:
    """
    Coordinates entity + relation stores
    """

    def __init__(self, entity_store, relation_store):
        self.entity_store = entity_store
        self.relation_store = relation_store