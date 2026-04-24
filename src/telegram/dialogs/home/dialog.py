# src/telegram/dialogs/home/dialog.py
# =========================================
# GROUP: telegram.dialogs.home
# FILE: dialog.py
# DESCRIPTION:
# Home dialog container (R3 base entry).
# =========================================

from aiogram_dialog import Dialog

from src.telegram.dialogs.home.window import home_window


home_dialog = Dialog(
    home_window
)