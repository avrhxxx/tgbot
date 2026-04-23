# src/bootstrap/app.py

from dataclasses import dataclass
from typing import Any

from src.engine.session_engine import SessionEngine, SessionData
from src.engine.state_machine import StateMachine


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
        # TYPE-SAFE CONTAINERS
        # =========================
        self.services: dict[str, object] = {}
        self.engines: dict[str, object] = {}
        self.ui: dict[str, object] = {}

        # =========================
        # CORE SYSTEMS
        # =========================
        self.state_machine = StateMachine()

        self.session_engine = SessionEngine(
            state_machine=self.state_machine
        )

    # =========================
    # SESSION HELPERS
    # =========================
    def get_session(self, user_id: str) -> SessionData:
        return self.session_engine.get(user_id)

    def set_session_state(self, user_id: str, state) -> None:
        self.session_engine.set_state(user_id, state)

    def set_session_nick(self, user_id: str, nick: str) -> None:
        self.session_engine.set_nick(user_id, nick)

    def get_session_nick(self, user_id: str) -> str | None:
        return self.session_engine.get_nick(user_id)

    def delete_session(self, user_id: str) -> None:
        self.session_engine.clear(user_id)

    # =========================
    # DEMO MODE
    # =========================
    def is_demo(self) -> bool:
        return self.demo_mode