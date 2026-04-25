# =========================================
# GROUP: telegram.dialogs.r4
# FILE: r4_dialog.py
# DESCRIPTION:
# R4 dialog registration.
# =========================================

import logging

from aiogram_dialog import Dialog

from src.telegram.windows.r4.r4 import r4_window

logger = logging.getLogger(__name__)


r4_dialog = Dialog(
    r4_window,
)