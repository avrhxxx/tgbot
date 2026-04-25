# =========================================
# GROUP: telegram.routing.capabilities
# FILE: role_ui_map.py
# DESCRIPTION:
# Central role → available routes mapping (NO UI logic)
# =========================================

from src.telegram.permissions.roles import Role

ROLE_UI_MAP: dict[Role, list[str]] = {
    Role.R3: ["home", "events", "help"],
    Role.R4: ["home", "events", "help", "r4_panel"],
    Role.R5: ["home", "events", "help", "r4_panel", "r5_panel"],
    Role.OWNER: ["home", "events", "help", "r4_panel", "r5_panel", "admin"],
}


def resolve_routes(role: Role) -> list[str]:
    return ROLE_UI_MAP.get(role, ["home"])