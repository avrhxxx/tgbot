# =========================================
# GROUP: telegram.windows.home
# FILE: settings.py
# =========================================

import logging
from typing import Any

from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Row, Button

from src.telegram.states.home import SettingsSG
from src.telegram.routing.core.binder import route_click

logger = logging.getLogger(__name__)


async def get_settings_data(dialog_manager: DialogManager, **kwargs: Any):
    logger.info("Rendering Settings window")

    return {
        "title": "Settings"
    }


settings_window = Window(
    Format(
        "⚙️ {title}\n\n"
        "User preferences coming soon."
    ),

    # 🔥 routing v2 navigation
    Row(
        Button(
            Format("⬅️ Back"),
            id="home",
            on_click=route_click("home"),
        ),
    ),

    getter=get_settings_data,
    state=SettingsSG.main,
)