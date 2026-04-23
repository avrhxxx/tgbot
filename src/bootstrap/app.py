# src/bootstrap/app.py

from dataclasses import dataclass
from typing import Any, Dict

from src.engine.state_machine import StateMachine
from src.engine.session_engine import SessionEngine

# =========================
# SCREEN SYSTEM
# =========================
from src.ui.screen_registry import ScreenRegistry
from src.ui.screen_router import ScreenRouter
from src.ui.bootstrap_screens import register_screens


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
        # STATE SYSTEM
        # =========================
        self.state_machine = StateMachine()

        # =========================
        # SESSION ENGINE
        # =========================
        self.session_engine = SessionEngine(
            state_machine=self.state_machine
        )

        # =========================
        # SCREEN SYSTEM INIT
        # =========================

        # 1. Registry
        self.screen_registry = ScreenRegistry()

        # 2. Register all screens
        register_screens(self.screen_registry)

        # 3. Router
        self.screen_router = ScreenRouter(self.screen_registry)

        # expose for services/handlers
        self.engines["screen_router"] = self.screen_router

    # =========================
    # SESSION HELPERS
    # =========================
    def get_session(self, user_id: str) -> dict:
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