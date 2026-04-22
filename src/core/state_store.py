from typing import Dict
from src.core.state import UIState


class StateStore:
    """
    SINGLE SOURCE OF TRUTH dla UI state + DEMO OVERRIDES
    """

    def __init__(self):
        self._store: Dict[int, UIState] = {}
        self._demo_role_override: Dict[int, str] = {}

    # =========================
    # UI STATE
    # =========================

    def get(self, user_id: int) -> UIState | None:
        return self._store.get(user_id)

    def set(self, user_id: int, state: UIState):
        self._store[user_id] = state

    def get_or_create(self, user_id: int, default: UIState) -> UIState:
        if user_id not in self._store:
            self._store[user_id] = default
        return self._store[user_id]

    # =========================
    # DEMO ROLE OVERRIDE
    # =========================

    def set_demo_role(self, user_id: int, role: str | None):
        if role is None:
            self._demo_role_override.pop(user_id, None)
        else:
            self._demo_role_override[user_id] = role

    def get_demo_role(self, user_id: int) -> str | None:
        return self._demo_role_override.get(user_id)

    def clear_demo_role(self, user_id: int):
        self._demo_role_override.pop(user_id, None)

    # =========================
    # CORE RESOLVER (NOWE)
    # =========================

    def get_effective_role(self, user_id: int, real_role: str) -> str:
        demo_role = self._demo_role_override.get(user_id)
        return demo_role if demo_role is not None else real_role


# GLOBAL INSTANCE
state_store = StateStore()