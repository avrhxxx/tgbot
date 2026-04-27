# =========================================
# FILE: src/handlers/start.py
# DESCRIPTION:
# Starts dialog properly (stable version)
# =========================================

from aiogram import Router, types
from aiogram_dialog import DialogManager, StartMode

from src.dialogs.panel.states import PanelSG
from src.utils.access import can_use_panel

router = Router()


@router.message()
async def start_handler(message: types.Message, dialog_manager: DialogManager):
    user = message.from_user

    if user is None:
        return

    if not can_use_panel(user.id):
        return

    # 🔥 ALWAYS RESET → no broken contexts
    await dialog_manager.start(
        PanelSG.main,
        mode=StartMode.RESET_STACK,
    )