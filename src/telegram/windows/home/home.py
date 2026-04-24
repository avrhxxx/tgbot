# =========================================
# GROUP: telegram.windows.home
# FILE: home.py
# DESCRIPTION:
# Home UI window (R3 dashboard)
# =========================================

import logging
from typing import Any

from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Row, Button

from src.telegram.dialogs.home.state import HomeSG

logger = logging.getLogger(__name__)


async def get_home_data(dialog_manager: DialogManager, **kwargs: Any):
    logger.info("Rendering Home window")
    return {
        "name": "User",
        "game_nick": "Not set",
        "role": "R3",
    }


home_window = Window(
    Format(
        "👋 Welcome\n\n"
        "🎮 Game Nick: {game_nick}\n"
        "🧭 Role: {role}"
    ),
    Row(
        Button(Format("📅 Events"), id="events"),
        Button(Format("⚙️ Settings"), id="settings"),
    ),
    Row(
        Button(Format("❓ Help"), id="help"),
    ),
    getter=get_home_data,
)