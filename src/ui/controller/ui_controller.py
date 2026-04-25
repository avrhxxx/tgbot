# =========================================
# GROUP: ui.controller
# FILE: ui_controller.py
# DESCRIPTION:
# Handles UI state transitions via event bus
# =========================================

from src.ui.state.ui_state import UIState
from src.ui.bus.events import NavigateEvent


class UIController:
    def __init__(self):
        self.state = UIState()

    def handle(self, event: NavigateEvent):
        self.state.screen = event.screen