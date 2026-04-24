# src/telegram/dialogs/home/window.py
# =========================================
# GROUP: telegram.dialogs.home
# FILE: window.py
# DESCRIPTION:
# R3 Home Window (base UI entry point).
# =========================================

from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Row, Button

from aiogram_dialog import DialogManager


async def get_home_data(dialog_manager: DialogManager, **kwargs):
    """
    Temporary mock data (later from DB/cache).
    """

    return {
        "name": dialog_manager.event.from_user.username
        or dialog_manager.event.from_user.first_name
        or "User",
        "game_nick": "Not set",
        "role": "R3",
    }


home_window = Window(
    Format(
        "👋 Welcome, {name}\n\n"
        "🎮 Game Nick: {game_nick}\n"
        "🧭 Role: {role}"
    ),
    Row(
        Button(Format("📅 Events"), id="events"),
        Button(Format("⚡ Quick Join"), id="quick_join"),
    ),
    Row(
        Button(Format("⚙️ Settings"), id="settings"),
        Button(Format("❓ Help"), id="help"),
    ),
    getter=get_home_data,
    state=None,  # placeholder (we add state later)
)