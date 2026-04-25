# =========================================
# GROUP: telegram.states
# FILE: register.py
# DESCRIPTION:
# FSM states for user onboarding / registration flow.
# =========================================

from aiogram.fsm.state import State, StatesGroup


class RegisterSG(StatesGroup):
    """
    Handles onboarding flow:
    - waiting for in-game nickname
    """

    waiting_for_nick = State()