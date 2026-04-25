# =========================================
# GROUP: ui.controller
# FILE: ui_controller.py
# DESCRIPTION:
# Event bus UI controller (single render engine)
# =========================================

import logging

from src.ui.state.ui_state import UIState

logger = logging.getLogger(__name__)


class UIController:
    def __init__(self):
        self.state = UIState()

    def set_screen(self, screen: str, payload: dict | None = None):
        """
        Safe state transition (no direct assignment typing issues)
        """
        logger.info("UI switch -> %s", screen)

        self.state.screen = screen  # type: ignore
        self.state.payload = payload

    def get_screen(self) -> str:
        return self.state.screen