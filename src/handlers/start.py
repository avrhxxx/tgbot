# =========================================
# FILE: src/handlers/start.py
# DESCRIPTION:
# Bot entry point → shows reply keyboard only
# =========================================

from aiogram import Router, types
from aiogram.filters import CommandStart

from src.dialogs.panel.dialog import panel_kb
from src.utils.access import can_use_panel

router = Router()


@router.message(CommandStart())
async def start_handler(message: types.Message):
    user = message.from_user

    if user is None:
        return

    if not can_use_panel(user.id):
        return

    # ONLY UI LAYER (no text, no dialog)
    await message.answer(
        " ",
        reply_markup=panel_kb
    )