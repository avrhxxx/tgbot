# =========================================
# GROUP: ui.state
# FILE: ui_state.py
# DESCRIPTION:
# Central UI state for Event Bus driven UI system
# =========================================

from dataclasses import dataclass
from typing import Literal, Optional


Screen = Literal["home", "settings", "events", "help"]


@dataclass
class UIState:
    screen: Screen = "home"
    user_id: Optional[int] = None