# =========================================
# GROUP: telegram.ui.core
# FILE: feature_resolver.py
# DESCRIPTION:
# Maps role -> UI feature modules.
# =========================================

from src.telegram.permissions.roles import Role


def resolve_features(screen: str, role: Role):
    """
    Returns feature list based on screen + role.
    """

    if screen == "home":
        return _home_features(role)

    return []


def _home_features(role: Role):

    # Base R3
    features = [
        {
            "buttons": [
                ("🏠 Home", "home"),
                ("🎮 Events", "events"),
                ("❓ Help", "help"),
            ]
        }
    ]

    # R4+
    if role in (Role.R4, Role.R5, Role.OWNER):
        features.append({
            "buttons": [
                ("📊 R4 PANEL", "events"),
            ]
        })

    # R5+
    if role in (Role.R5, Role.OWNER):
        features.append({
            "buttons": [
                ("🛡 R5 PANEL", "settings"),
            ]
        })

    return features