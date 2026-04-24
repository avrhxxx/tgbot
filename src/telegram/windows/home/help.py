# =========================================
# GROUP: telegram.windows.home
# FILE: help.py
# =========================================

import logging

from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Row, Button

from src.telegram.states.home import HelpSG
from src.telegram.routing.core.binder import route_click

logger = logging.getLogger(__name__)


async def get_help_data(dialog_manager: DialogManager, **kwargs):
    logger.info("Rendering Help window")

    return {}


help_window = Window(
    Format(
        "❓ Help\n\n"
        "FAQ / support coming soon.\n"
        "If you are stuck, go back to Home."
    ),

    # 🔥 routing v2 navigation
    Row(
        Button(
            Format("⬅️ Back"),
            id="home",
            on_click=route_click("home"),
        ),
    ),

    getter=get_help_data,
    state=HelpSG.main,
)