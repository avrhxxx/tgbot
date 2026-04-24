# =========================================
# GROUP: telegram.dialogs.home
# FILE: dialog.py
# DESCRIPTION:
# Home dialog container (R3 base entry).
# =========================================

import logging
from aiogram_dialog import Dialog

from src.telegram.dialogs.home.window import home_window
from src.telegram.dialogs.home.events import events_window
from src.telegram.dialogs.home.settings import settings_window
from src.telegram.dialogs.home.help import help_window


logger = logging.getLogger(__name__)


home_dialog = Dialog(
    home_window,
    events_window,
    settings_window,
    help_window,
)


logger.info("Home dialog initialized with full window stack")