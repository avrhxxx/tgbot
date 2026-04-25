# =========================================
# GROUP: telegram.dialogs.home
# FILE: home_dialog.py
# DESCRIPTION:
# Dialog binding for Home screen (NO logic here)
# =========================================

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Row, Button

from src.telegram.states.home import HomeSG

from src.telegram.windows.home.home import get_home_data
from src.telegram.components.home_buttons import build_home_buttons
from src.telegram.ui.navigation.home_nav import navigate


def _build_buttons():
    """
    Static wrapper for aiogram-dialog Button binding.
    Role logic stays in components.
    """

    return [
        Button("🏠 Home", id="home", on_click=lambda c, b, m: navigate("home", m)),
        Button("🎮 Events", id="events", on_click=lambda c, b, m: navigate("events", m)),
        Button("⚙️ Settings", id="settings", on_click=lambda c, b, m: navigate("settings", m)),
        Button("❓ Help", id="help", on_click=lambda c, b, m: navigate("help", m)),
    ]


home_window = Window(
    Format("{text}"),
    Row(*_build_buttons()),
    state=HomeSG.main,
    getter=get_home_data,
)

home_dialog = Dialog(home_window)