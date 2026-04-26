# src/dialogs/panel/states.py

from aiogram.fsm.state import StatesGroup, State


class PanelSG(StatesGroup):
    main = State()
    broadcast_menu = State()

    broadcast_title = State()
    broadcast_tags = State()
    broadcast_text = State()
    broadcast_confirm = State()