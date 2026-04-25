# =========================================
# GROUP: telegram.windows.home
# FILE: home_window.py
# DESCRIPTION:
# PURE UI window (NO role logic)
# =========================================

from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Row, Button

from src.telegram.states.home import HomeSG
from src.telegram.windows.home.home import get_home_data

from src.telegram.ui.core.ui_composer import ui_composer
from src.telegram.permissions.context import UserContext


def build_home_keyboard(user: UserContext):

    base_buttons = [
        (("🏠 Home", "home")),
        (("🎮 Events", "events")),
        (("❓ Help", "help")),
    ]

    composed = ui_composer.compose_home(
        user=user,
        base_text="{text}",
        base_buttons=base_buttons,
    )

    rows = []

    for label, route in composed["buttons"]:
        rows.append(Button(label, id=route))

    return [Row(*rows)]


home_window = Window(
    Format("{text}"),
    state=HomeSG.main,
    getter=get_home_data,
)