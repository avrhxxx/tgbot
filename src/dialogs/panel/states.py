# src/dialogs/panel/states.py
# DESCRIPTION:
# Dialog states for moderator panel.

from aiogram.fsm.state import StatesGroup, State


class PanelSG(StatesGroup):
    main = State()