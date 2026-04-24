# src/telegram/dialogs/home/window.py
# =========================================
# GROUP: telegram.dialogs.home
# FILE: window.py
# DESCRIPTION:
# R3 Home Window (base UI entry point).
# =========================================

from typing import Any

from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Row, Button


async def get_home_data(dialog_manager: DialogManager, **kwargs: Any):
    """
    Temporary mock data (later from DB/cache).
    """

    event = getattr(dialog_manager, "event", None)
    user = getattr(event, "from_user", None) if event else None

    name = (
        getattr(user, "username", None)
        or getattr(user, "first_name", None)
        or "User"
    )

    return {
        "name": name,
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
    # state zostanie podpięte przez Dialog (nie tutaj)
)