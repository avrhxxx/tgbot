# =========================================
# GROUP: telegram.dialogs.home
# FILE: help_dialog.py
# DESCRIPTION:
# Help dialog (placeholder)
# =========================================

import logging
from aiogram_dialog import Dialog

from src.telegram.windows.home.help import help_window

logger = logging.getLogger(__name__)


help_dialog = Dialog(
    help_window,
)

logger.info("Help dialog registered")