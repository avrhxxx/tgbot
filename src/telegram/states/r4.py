# =========================================
# GROUP: telegram.states
# FILE: r4.py
# DESCRIPTION:
# R4 (Officer) panel state definition.
# =========================================

from aiogram.fsm.state import StatesGroup, State


class R4SG(StatesGroup):
    main = State()