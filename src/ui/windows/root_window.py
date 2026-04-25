# =========================================
# GROUP: ui.windows
# FILE: root_window.py
# DESCRIPTION:
# Single dynamic window (NO MULTIPLE WINDOWS)
# =========================================

from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Row, Button

from src.telegram.states.home import HomeSG

from src.ui.state.ui_state import UIState
from src.ui.render.home import render_home
from src.ui.render.settings import render_settings


def get_ui_data(dialog_manager, **kwargs):
    state: UIState = dialog_manager.middleware_data["ui_state"]

    if state.screen == "home":
        return render_home(state)

    if state.screen == "settings":
        return render_settings(state)

    return {"text": "Unknown screen", "keyboard": None}


def nav(screen: str):
    async def _cb(_, __, manager):
        state: UIState = manager.middleware_data["ui_state"]
        state.screen = screen
        await manager.switch_to(HomeSG.main)

    return _cb


root_window = Window(
    Format("{text}"),

    Row(
        Button("🏠 Home", id="home", on_click=nav("home")),
        Button("⚙️ Settings", id="settings", on_click=nav("settings")),
    ),

    state=HomeSG.main,
    getter=get_ui_data,
)