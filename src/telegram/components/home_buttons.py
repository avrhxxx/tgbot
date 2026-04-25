# =========================================
# GROUP: telegram.components
# FILE: home_buttons.py
# DESCRIPTION:
# Role-aware UI builder using policy.py (NOT hardcoded roles)
# =========================================

from dataclasses import dataclass
from typing import List

from src.telegram.permissions.policy import get_permission
from src.telegram.permissions.context import UserContext


@dataclass
class Button:
    label: str
    route: str


def can_show(user: UserContext, route_id: str) -> bool:
    return get_permission(route_id).allows(user.role)


def build_home_buttons(user: UserContext) -> List[Button]:

    buttons = [
        Button("🏠 Home", "home"),
        Button("🎮 Events", "events"),
        Button("❓ Help", "help"),
    ]

    # R4 / R5
    if can_show(user, "events"):
        buttons.append(Button("📊 R4 PANEL", "events"))

    # R5 only (settings access level)
    if can_show(user, "settings"):
        buttons.append(Button("🛡 R5 PANEL", "settings"))

    return buttons