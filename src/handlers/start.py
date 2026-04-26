# src/handlers/start.py
# DESCRIPTION:
# Entry point for moderator/admin panel.

from aiogram import Router, types

from src.utils.access import can_use_panel

router = Router()


@router.message(lambda m: m.text == "/start")
async def start_handler(message: types.Message):
    user = message.from_user

    if user is None:
        await message.answer("❌ Unable to identify user.")
        return

    user_id = user.id

    if not can_use_panel(user_id):
        await message.answer("❌ No access.")
        return

    await message.answer(
        "🛠 MODERATOR PANEL\n\n"
        "📌 Available actions:\n"
        "• /broadcast - create broadcast message"
    )