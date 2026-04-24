# =========================================
# GROUP: telegram.dialogs.home
# FILE: events.py
# DESCRIPTION:
# Events UI window (placeholder screen).
# =========================================

import logging
from typing import Any

from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Row, Button

from src.telegram.dialogs.home.routing import HOME
from src.telegram.dialogs.home.state import HomeSG

logger = logging.getLogger(__name__)


async def get_events_data(**kwargs: Any):
    logger.info("Rendering Events window (placeholder)")
    return {
        "title": "Events",
    }


events_window = Window(
    Format(
        "📅 {title}\n\n"
        "No events available yet."
    ),
    Row(
        Button(Format("⬅️ Back"), id=HOME),
    ),
    getter=get_events_data,
    state=HomeSG.main,
)