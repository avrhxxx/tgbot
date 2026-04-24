# =========================================
# GROUP: telegram.dialogs.home
# FILE: dialog.py
# DESCRIPTION:
# Home dialog container (R3 base entry).
# =========================================

import logging
from aiogram_dialog import Dialog

from src.telegram.dialogs.home.window import home_window
from src.telegram.dialogs.home.state import HomeSG

logger = logging.getLogger(__name__)


home_dialog = Dialog(
    home_window,
)


logger.info("Home dialog initialized (single window mode)")