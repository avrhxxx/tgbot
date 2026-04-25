# =========================================
# GROUP: telegram.components.menu
# FILE: menu_resolver.py
# DESCRIPTION:
# Role-aware menu route resolver (NO UI, NO buttons)
# =========================================

from typing import List

from src.telegram.permissions.policy import get_permission
from src.telegram.permissions.context import UserContext


def can_show(user: UserContext, route_id: str) -> bool:
    return get_permission(route_id).allows(user.role)


def build_home_routes(user: UserContext) -> List[str]:
    """
    Returns list of available route IDs for HOME menu.
    UI layer decides how to render them.
    """

    routes: List[str] = [
        "home",
        "events",
        "help",
    ]

    if can_show(user, "settings"):
        routes.append("settings")

    # R4/R5 future panels (optional expansion point)
    if can_show(user, "events"):
        routes.append("events")

    return routes