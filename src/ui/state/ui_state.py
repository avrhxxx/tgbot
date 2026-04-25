# =========================================
# GROUP: ui.state
# FILE: ui_state.py
# DESCRIPTION:
# Central UI state machine (event-driven navigation)
# =========================================

from dataclasses import dataclass
from typing import Literal


ScreenType = Literal["home", "settings", "events", "help"]


@dataclass
class UIState:
    screen: ScreenType = "home"
    payload: dict | None = None