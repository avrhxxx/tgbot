# =========================================
# GROUP: telegram.dialogs.register
# FILE: register_dialog.py
# DESCRIPTION:
# Aiogram-dialog wrapper for Register window.
# =========================================

import logging
from aiogram_dialog import Dialog

from src.telegram.windows.register.register import register_window

logger = logging.getLogger(__name__)

register_dialog = Dialog(
    register_window,
)

logger.info("Register dialog initialized")