# =========================================
# FILE: src/dialogs/group_message/states.py
# =========================================

from aiogram.fsm.state import StatesGroup, State


class GroupMessageSG(StatesGroup):
    input = State()
    preview = State()