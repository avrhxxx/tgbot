# =========================================
# GROUP: telegram.dialogs.home
# FILE: settings_dialog.py
# DESCRIPTION:
# Settings dialog (placeholder)
# =========================================

import logging
from aiogram_dialog import Dialog

from src.telegram.dialogs.home.settings import settings_window
from src.telegram.dialogs.home.state import SettingsSG

logger = logging.getLogger(__name__)


settings_dialog = Dialog(
    settings_window,
)

logger.info("Settings dialog registered")