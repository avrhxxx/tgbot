# =========================================
# GROUP: telegram.components
# FILE: home_buttons.py
# DESCRIPTION:
# Role-aware dynamic button builder for Home screen.
# =========================================

from dataclasses import dataclass
from typing import List

from src.services.user.user_profile import user_profile


@dataclass
class Button:
    label: str
    route: str


def build_home_buttons(user_id: int) -> List[Button]:
    profile = user_profile.get(user_id)

    role = profile.role if profile else "R3"

    buttons = [
        Button("🏠 Home", "home"),
        Button("🎮 Events", "events"),
        Button("❓ Help", "help"),
    ]

    # R4 / R5 shared access
    if role in ["R4", "R5"]:
        buttons.append(Button("📊 R4 PANEL", "events"))

    # R5 ONLY
    if role == "R5":
        buttons.append(Button("🛡 R5 PANEL", "settings"))

    return buttons