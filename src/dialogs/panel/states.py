# =========================================
# FILE: src/dialogs/panel/states.py
# DESCRIPTION:
# States for moderator panel announcement wizard
# =========================================

from aiogram.fsm.state import StatesGroup, State


class PanelSG(StatesGroup):
    # =========================
    # MAIN PANEL
    # =========================
    main = State()

    # =========================
    # ANNOUNCEMENT FLOW
    # =========================
    announcement_menu = State()
    create_tag = State()  # 🔥 dodany brakujący state

    announcement_title = State()
    announcement_content = State()
    announcement_preview = State()