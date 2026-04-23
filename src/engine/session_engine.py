# src/engine/session_engine.py

from dataclasses import dataclass
from typing import Optional, TypedDict, cast

from src.engine.state_machine import StateMachine, UserState
from src.storage.session_cache import SESSION_CACHE


# =========================
# SESSION MODEL (STRICT)
# =========================
class SessionData(TypedDict):
    state: UserState
    game_nick: Optional[str]


# =========================
# SESSION ENGINE
# =========================
@dataclass
class SessionEngine:
    """
    Central user session manager.

    Uses:
    - cachetools TTLCache (in-memory global store)
    - state machine validation
    """

    state_machine: StateMachine

    # =========================
    # GET SESSION
    # =========================
    def get(self, user_id: str) -> SessionData:
        if user_id not in SESSION_CACHE:
            SESSION_CACHE[user_id] = {
                "state": UserState.NEW,
                "game_nick": None,
            }

        return cast(SessionData, SESSION_CACHE[user_id])

    # =========================
    # STATE HANDLING
    # =========================
    def get_state(self, user_id: str) -> UserState:
        return self.get(user_id)["state"]

    def set_state(self, user_id: str, new_state: UserState) -> None:
        session = self.get(user_id)
        current = session["state"]

        validated = self.state_machine.transition(current, new_state)
        session["state"] = validated

    # =========================
    # NICK HANDLING
    # =========================
    def get_nick(self, user_id: str) -> Optional[str]:
        return self.get(user_id)["game_nick"]

    def set_nick(self, user_id: str, nick: str) -> None:
        self.get(user_id)["game_nick"] = nick

    # =========================
    # RESET SESSION
    # =========================
    def clear(self, user_id: str) -> None:
        SESSION_CACHE.pop(user_id, None)