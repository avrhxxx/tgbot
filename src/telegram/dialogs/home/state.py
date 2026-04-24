# src/telegram/dialogs/home/state.py
# =========================================
# GROUP: telegram.dialogs.home
# FILE: state.py
# DESCRIPTION:
# FSM states for Home dialog (R3 base UI).
# =========================================

from aiogram.fsm.state import State, StatesGroup


class HomeSG(StatesGroup):
    """
    States for Home screen dialog.
    """
    main = State()