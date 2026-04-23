# src/engine/session_engine.py

from dataclasses import dataclass
from typing import Dict, Optional

from src.engine.state_machine import StateMachine, UserState


# =========================
# SESSION ENGINE
# =========================
@dataclass
class SessionEngine:
    """
    Central user session manager.

    Wraps:
    - in-memory storage
    - state machine rules
    """

    store: Dict[str, dict]
    state_machine: StateMachine

    # =========================
    # GET SESSION
    # =========================
    def get(self, user_id: str) -> dict:
        if user_id not in self.store:
            self.store[user_id] = {
                "state": UserState.NEW,
                "game_nick": None,
            }
        return self.store[user_id]

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
        return self.get(user_id).get("game_nick")

    def set_nick(self, user_id: str, nick: str) -> None:
        self.get(user_id)["game_nick"] = nick

    # =========================
    # RESET SESSION
    # =========================
    def clear(self, user_id: str) -> None:
        if user_id in self.store:
            del self.store[user_id]