# src/bootstrap/app.py

from dataclasses import dataclass
from typing import Any, Dict


# =========================
# SHADOW BOT RUNTIME CONTEXT
# =========================
@dataclass
class AppContext:
    """
    Central runtime container for Shadow Bot.

    Holds:
    - config
    - demo mode flag
    - in-memory sessions
    - service registry
    - engine registry
    - UI registry
    """

    config: Any

    def __post_init__(self):
        # =========================
        # DEMO MODE SWITCH
        # =========================
        self.demo_mode: bool = self.config.features.demo_mode

        # =========================
        # IN-MEMORY SESSION STORE (MVP)
        # =========================
        self.sessions: Dict[str, dict] = {}

        # =========================
        # SERVICE REGISTRY
        # =========================
        self.services: Dict[str, Any] = {}

        # =========================
        # ENGINE REGISTRY
        # =========================
        self.engines: Dict[str, Any] = {}

        # =========================
        # UI REGISTRY (screens/keyboards/renderers)
        # =========================
        self.ui: Dict[str, Any] = {}

    # =========================
    # SESSION HELPERS
    # =========================
    def get_session(self, user_id: str) -> dict | None:
        return self.sessions.get(user_id)

    def set_session(self, user_id: str, data: dict) -> None:
        self.sessions[user_id] = data

    def delete_session(self, user_id: str) -> None:
        if user_id in self.sessions:
            del self.sessions[user_id]

    # =========================
    # DEMO MODE GUARD
    # =========================
    def is_demo(self) -> bool:
        return self.demo_mode