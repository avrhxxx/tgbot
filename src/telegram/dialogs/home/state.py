# =========================================
# GROUP: telegram.dialogs.home
# FILE: state.py
# DESCRIPTION:
# FSM states for Home module (R3 UI flow).
# Each window must have unique state (aiogram-dialog requirement).
# =========================================

from aiogram.fsm.state import State, StatesGroup


class HomeSG(StatesGroup):
    """
    Home dashboard entry window.
    """
    main = State()


class EventsSG(StatesGroup):
    """
    Events list window.
    """
    main = State()


class SettingsSG(StatesGroup):
    """
    Settings window.
    """
    main = State()


class HelpSG(StatesGroup):
    """
    Help / FAQ window.
    """
    main = State()