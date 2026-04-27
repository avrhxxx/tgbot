# =========================================
# FILE: src/dialogs/main_menu/states.py
# DESCRIPTION:
# Main menu dialog states (UI navigation only)
# =========================================

from aiogram.fsm.state import StatesGroup, State


class MainMenuSG(StatesGroup):
    main = State()
    group_message = State()
    event_manager = State()
    language = State()