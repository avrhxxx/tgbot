# src/bootstrap/app.py

from dataclasses import dataclass
from typing import Any, Dict

from src.engine.state_machine import StateMachine
from src.engine.session_engine import SessionEngine


# =========================
# SHADOW BOT RUNTIME CONTEXT
# =========================
@dataclass
class AppContext:
    """
    Central runtime container for Shadow Bot.
    """

    config: Any

    def __post_init__(self):
        # =========================
        # DEMO MODE
        # =========================
        self.demo_mode: bool = self.config.features.demo_mode

        # =========================
        # REGISTRIES
        # =========================
        self.services: Dict[str, Any] = {}
        self.engines: Dict[str, Any] = {}
        self.ui: Dict[str, Any] = {}

        # =========================
        # STATE SYSTEM (NEW CORE)
        # =========================
        self.state_machine = StateMachine()

        self.session_engine = SessionEngine(
            store={},
            state_machine=self.state_machine
        )

    # =========================
    # SESSION HELPERS (WRAPPED)
    # =========================
    def get_session(self, user_id: str) -> dict:
        return self.session_engine.get(user_id)

    def set_session(self, user_id: str, data: dict) -> None:
        self.session_engine.store[user_id] = data

    def delete_session(self, user_id: str) -> None:
        self.session_engine.clear(user_id)

    # =========================
    # DEMO MODE
    # =========================
    def is_demo(self) -> bool:
        return self.demo_mode