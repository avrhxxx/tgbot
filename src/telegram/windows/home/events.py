# =========================================
# GROUP: telegram.windows.home
# FILE: events.py
# =========================================

import logging
from typing import Any

from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Row, Button

logger = logging.getLogger(__name__)


async def get_events_data(**kwargs: Any):
    logger.info("Rendering Events window")
    return {"title": "Events"}


events_window = Window(
    Format("📅 {title}\n\nNo events yet."),
    Row(Button(Format("⬅️ Back"), id="home")),
    getter=get_events_data,
)