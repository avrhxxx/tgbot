# =========================================
# GROUP: handlers
# FILE: start.py
# DESCRIPTION:
# Entry point for moderator/admin panel.
# =========================================

from aiogram import Router, types
from src.utils.access import can_use_panel

router = Router()


@router.message(lambda m: m.text == "/start")
async def start_handler(message: types.Message):
    user_id = message.from_user.id

    if not can_use_panel(user_id):
        await message.answer("❌ No access.")
        return

    await message.answer(
        "🛠 MODERATOR PANEL\n\n"
        "📌 Available actions:\n"
        "• /broadcast - create broadcast message"
    )