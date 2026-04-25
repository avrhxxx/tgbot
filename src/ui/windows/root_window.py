from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Row, Button

from src.ui.state.ui_state import UIState


def nav(screen: str, ui):
    ui.set_screen(screen)


root_window = Window(
    Format("🏠 HOME"),
    Row(
        Button(text=Format("🏠 Home"), id="home"),
        Button(text=Format("🎮 Events"), id="events"),
    ),
    Row(
        Button(text=Format("⚙️ Settings"), id="settings"),
        Button(text=Format("❓ Help"), id="help"),
    ),
    state=UIState,
)