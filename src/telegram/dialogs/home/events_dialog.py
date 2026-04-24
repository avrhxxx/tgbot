# =========================================
# GROUP: telegram.dialogs.home
# FILE: events_dialog.py
# DESCRIPTION:
# Events dialog (placeholder)
# =========================================

import logging
from aiogram_dialog import Dialog

from src.telegram.dialogs.home.events import events_window
from src.telegram.dialogs.home.state import EventsSG

logger = logging.getLogger(__name__)


events_dialog = Dialog(
    events_window,
)

logger.info("Events dialog registered")