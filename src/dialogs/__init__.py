# =========================================
# FILE: src/dialogs/__init__.py
# =========================================

from aiogram import Dispatcher

from src.dialogs.main_menu.dialog import main_menu_dialog


def register_dialogs(dp: Dispatcher):
    dp.include_router(main_menu_dialog)