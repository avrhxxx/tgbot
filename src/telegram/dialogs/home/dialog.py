# src/telegram/dialogs/home/dialog.py
# =========================================
# GROUP: telegram.dialogs.home
# FILE: dialog.py
# DESCRIPTION:
# Home dialog container (R3 base entry).
# =========================================

import logging
from aiogram_dialog import Dialog

from src.telegram.dialogs.home.window import home_window


logger = logging.getLogger(__name__)


home_dialog = Dialog(
    home_window
)

logger.info("Home dialog registered (R3 entry window)")