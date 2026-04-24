# =========================================
# GROUP: telegram.dialogs.home
# FILE: home_dialog.py
# DESCRIPTION:
# Home entry dialog (R3 dashboard)
# =========================================

import logging
from aiogram_dialog import Dialog

from src.telegram.windows.home.home import home_window
from src.telegram.dialogs.home.state import HomeSG

logger = logging.getLogger(__name__)


home_dialog = Dialog(
    home_window,
)

logger.info("Home dialog registered")