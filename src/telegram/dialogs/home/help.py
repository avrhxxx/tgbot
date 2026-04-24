# =========================================
# GROUP: telegram.dialogs.home
# FILE: help.py
# DESCRIPTION:
# Help UI window (placeholder screen).
# =========================================

import logging

from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Row, Button

from src.telegram.dialogs.home.routing import HOME
from src.telegram.dialogs.home.state import HomeSG

logger = logging.getLogger(__name__)


logger.info("Help window module loaded")


help_window = Window(
    Format(
        "❓ Help\n\n"
        "Here will be FAQ / support info."
    ),
    Row(
        Button(Format("⬅️ Back"), id=HOME),
    ),
    state=HomeSG.main,
)