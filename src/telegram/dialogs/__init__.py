# src/telegram/dialogs/__init__.py
# =========================================
# GROUP: telegram.dialogs
# FILE: __init__.py
# DESCRIPTION:
# Dialog registration entry point.
# =========================================

from aiogram_dialog import setup_dialogs

from src.telegram.dialogs.home.dialog import home_dialog


def setup_all_dialogs(dp):
    dp.include_router(home_dialog)
    setup_dialogs(dp)