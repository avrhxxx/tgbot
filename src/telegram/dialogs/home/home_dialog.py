# =========================================
# GROUP: telegram.dialogs.home
# FILE: home_dialog.py
# =========================================

from aiogram_dialog import Dialog

from src.telegram.windows.home.home_window import home_window
from src.telegram.windows.home.settings_window import settings_window

home_dialog = Dialog(
    home_window,
    settings_window,
)