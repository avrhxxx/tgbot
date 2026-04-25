# =========================================
# GROUP: telegram.components
# FILE: home_buttons.py
# =========================================

from typing import List


def build_home_buttons(routes: list[str]) -> List[list]:
    """
    Returns aiogram-dialog compatible keyboard rows
    (NO dataclasses, NO UI logic, NO roles)
    """

    buttons = []

    if "home" in routes:
        buttons.append(["🏠 Home"])

    if "events" in routes:
        buttons.append(["🎮 Events"])

    if "settings" in routes:
        buttons.append(["⚙️ Settings"])

    if "help" in routes:
        buttons.append(["❓ Help"])

    if "r4_panel" in routes:
        buttons.append(["📊 R4 PANEL"])

    if "r5_panel" in routes:
        buttons.append(["🛡 R5 PANEL"])

    return buttons