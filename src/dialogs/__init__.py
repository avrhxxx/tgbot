# =========================================
# FILE: src/dialogs/__init__.py
# =========================================

from aiogram import Dispatcher

from src.dialogs.main_menu.dialog import main_menu_dialog
from src.dialogs.group_message.dialog import group_message_dialog
from src.dialogs.event_manager.dialog import event_manager_dialog  # 👈 DODAJ


def register_dialogs(dp: Dispatcher):
    dp.include_router(main_menu_dialog)
    dp.include_router(group_message_dialog)
    dp.include_router(event_manager_dialog)  # 👈 DODAJ