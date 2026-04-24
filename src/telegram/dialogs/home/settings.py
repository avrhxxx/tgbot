# =========================================
# GROUP: telegram.dialogs.home
# FILE: settings.py
# DESCRIPTION:
# Settings UI window (placeholder screen).
# =========================================

import logging

from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Row, Button

from src.telegram.dialogs.home.routing import HOME

logger = logging.getLogger(__name__)


logger.info("Settings window module loaded")


settings_window = Window(
    Format(
        "⚙️ Settings\n\n"
        "User preferences will appear here."
    ),
    Row(
        Button(Format("⬅️ Back"), id=HOME),
    ),
)