# src/dialogs/panel/states.py
# =========================================
# FILE: src/dialogs/panel/states.py
# DESCRIPTION:
# States for moderator panel broadcast wizard (MVP)
# =========================================

from aiogram.fsm.state import StatesGroup, State


class PanelSG(StatesGroup):
    # =========================
    # MAIN PANEL
    # =========================
    main = State()

    # =========================
    # BROADCAST FLOW
    # =========================
    broadcast_menu = State()      # tag selection
    broadcast_title = State()     # title input
    broadcast_content = State()   # message input
    broadcast_preview = State()   # final preview