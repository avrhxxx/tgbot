# =========================================
# GROUP: telegram.windows.r4
# FILE: r4.py
# DESCRIPTION:
# R4 panel window (Officer UI).
# =========================================

import logging

from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Row, Button

from src.telegram.states.r4 import R4SG
from src.telegram.routing.core.binder import route_click

logger = logging.getLogger(__name__)


r4_window = Window(
    Format(
        "🛡 R4 PANEL\n\n"
        "Officer tools will be here."
    ),

    Row(
        Button(
            Format("⬅️ Back"),
            id="back",
            on_click=route_click("home"),
        )
    ),

    state=R4SG.main,
)