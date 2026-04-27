# =========================================
# FILE: src/handlers/start.py
# DESCRIPTION:
# Bot entry point → shows reply keyboard only (silent)
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

    # 🔥 Silent message (invisible char required by Telegram)
    await message.answer(
        "‎",  # ZERO WIDTH SPACE
        reply_markup=panel_kb
    )