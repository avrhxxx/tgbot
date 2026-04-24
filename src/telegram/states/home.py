# =========================================
# GROUP: telegram.states.home
# FILE: home.py
# DESCRIPTION:
# FSM states for Home module.
# =========================================

from aiogram.fsm.state import State, StatesGroup


class HomeSG(StatesGroup):
    main = State()


class EventsSG(StatesGroup):
    main = State()


class SettingsSG(StatesGroup):
    main = State()


class HelpSG(StatesGroup):
    main = State()