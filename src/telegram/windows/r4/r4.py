# =========================================
# GROUP: telegram.windows.r4
# FILE: r4.py
# DESCRIPTION:
# R4 panel UI window (Officer dashboard).
# =========================================

import logging

from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Row, Button

from src.telegram.states.r4 import R4SG
from src.telegram.routing.core.binder import route_click

logger = logging.getLogger(__name__)


async def get_r4_data(**kwargs):
    logger.info("Rendering R4 window")
    return {}


r4_window = Window(
    Format(
        "🛡 R4 PANEL\n\n"
        "Officer dashboard\n"
    ),

    # BACK (wraca do HOME)
    Row(
        Button(
            Format("⬅️ Back"),
            id="back",
            on_click=route_click("home"),
        )
    ),

    getter=get_r4_data,
    state=R4SG.main,
)