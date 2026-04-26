# src/dialogs/panel/states.py

from aiogram.fsm.state import StatesGroup, State


class PanelSG(StatesGroup):
    main = State()
    broadcast_menu = State()