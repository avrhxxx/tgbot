# =========================================
# FILE: src/dialogs/group_message/states.py
# =========================================

from aiogram_dialog import StatesGroup, State


class GroupMessageSG(StatesGroup):
    input = State()
    preview = State()