# =========================================
# GROUP: telegram.dialogs.home
# FILE: home_dialog.py
# =========================================

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Button

from src.telegram.states.home import HomeSG
from src.telegram.windows.home.home import get_home_data  # 🔥 FIX GETTER


home_window = Window(
    Format("{text}"),
    state=HomeSG.main,
    getter=get_home_data,
)

home_dialog = Dialog(home_window)