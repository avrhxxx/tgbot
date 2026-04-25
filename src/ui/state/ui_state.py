# =========================================
# GROUP: ui.state
# FILE: ui_state.py
# =========================================

from dataclasses import dataclass
from typing import Literal, Optional


Screen = Literal["home", "settings", "events", "help"]


@dataclass
class UIState:
    screen: Screen = "home"
    message_id: Optional[int] = None