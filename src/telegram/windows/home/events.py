# =========================================
# GROUP: telegram.windows.home
# FILE: events.py
# =========================================

import logging
from typing import Any

from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Row, Button

from src.telegram.states.home import EventsSG
from src.telegram.routing.core.binder import route_click

logger = logging.getLogger(__name__)


async def get_events_data(dialog_manager: DialogManager, **kwargs: Any):
    logger.info("Rendering Events window")

    # 🔥 placeholder data layer (future: event service)
    return {
        "title": "Events"
    }


events_window = Window(
    Format(
        "📅 {title}\n\n"
        "No events yet.\n"
        "Stay tuned."
    ),

    # 🔥 NAVIGATION (routing v2)
    Row(
        Button(
            Format("⬅️ Back"),
            id="home",
            on_click=route_click("home"),
        ),
    ),

    getter=get_events_data,
    state=EventsSG.main,
)