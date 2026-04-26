# src/handlers/start.py
# DESCRIPTION:
# Starts moderator panel dialog.

from aiogram import Router, types
from aiogram_dialog import DialogManager, StartMode

from src.dialogs.panel.states import PanelSG
from src.utils.access import can_use_panel

router = Router()


@router.message(lambda m: m.text == "/start")
async def start_handler(message: types.Message, dialog_manager: DialogManager):
    user = message.from_user

    if user is None:
        await message.answer("❌ Unable to identify user.")
        return

    if not can_use_panel(user.id):
        await message.answer("❌ No access.")
        return

    await dialog_manager.start(
        PanelSG.main,
        mode=StartMode.RESET_STACK,
    )