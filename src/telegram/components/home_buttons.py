# =========================================
# GROUP: telegram.components
# FILE: home_buttons.py
# DESCRIPTION:
# Pure UI builder (NO roles, NO permissions)
# =========================================

from dataclasses import dataclass
from typing import List


@dataclass
class Button:
    label: str
    route: str


BUTTON_LABELS = {
    "home": "🏠 Home",
    "events": "🎮 Events",
    "help": "❓ Help",
    "r4_panel": "📊 R4 PANEL",
    "r5_panel": "🛡 R5 PANEL",
    "admin": "⚙️ ADMIN",
}


def build_home_buttons(routes: list[str]) -> List[Button]:
    return [
        Button(BUTTON_LABELS[r], r)
        for r in routes
        if r in BUTTON_LABELS
    ]