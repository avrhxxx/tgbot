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

from src.telegram.states.home import HomeSG
from src.telegram.routing.core.binder import route_click

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
        "👋 Welcome, {name}\n\n"
        "🎮 Game Nick: {game_nick}\n"
        "🧭 Role: {role}"
    ),

    # 🔥 QUICK JOIN (wrócił)
    Row(
        Button(
            Format("⚡ Quick Join"),
            id="quick_join",
            on_click=route_click("quick_join"),
        ),
    ),

    Row(
        Button(
            Format("📅 Events"),
            id="events",
            on_click=route_click("events"),
        ),
        Button(
            Format("⚙️ Settings"),
            id="settings",
            on_click=route_click("settings"),
        ),
    ),
    Row(
        Button(
            Format("❓ Help"),
            id="help",
            on_click=route_click("help"),
        ),
    ),
    getter=get_home_data,
    state=HomeSG.main,
)