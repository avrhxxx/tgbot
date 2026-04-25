# =========================================
# GROUP: telegram.dialogs.home
# FILE: settings_dialog.py
# =========================================

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format

from src.telegram.states.home import SettingsSG
from src.telegram.windows.home.settings import get_settings_data  # 🔥 FIX


settings_window = Window(
    Format("{text}"),
    state=SettingsSG.main,
    getter=get_settings_data,
)

settings_dialog = Dialog(settings_window)