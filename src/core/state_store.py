from typing import Dict
from src.core.state import UIState

class StateStore:
    """
    SINGLE SOURCE OF TRUTH dla UI state
    """

    def __init__(self):
        self._store: Dict[int, UIState] = {}

    def get(self, user_id: int) -> UIState | None:
        return self._store.get(user_id)

    def set(self, user_id: int, state: UIState):
        self._store[user_id] = state

    def get_or_create(self, user_id: int, default: UIState) -> UIState:
        if user_id not in self._store:
            self._store[user_id] = default
        return self._store[user_id]


# GLOBAL INSTANCE (MVP)
state_store = StateStore()