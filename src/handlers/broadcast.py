# =========================================
# GROUP: handlers
# FILE: broadcast.py
# DESCRIPTION:
# Simple broadcast flow (FSM-less MVP version).
# =========================================

from aiogram import Router, types
from src.utils.access import is_mod, get_chat_ids

router = Router()

_pending = set()


@router.message(lambda m: m.text == "/broadcast")
async def start_broadcast(message: types.Message):
    user_id = message.from_user.id

    if not is_mod(user_id):
        await message.answer("❌ No access.")
        return

    _pending.add(user_id)

    await message.answer(
        "📣 Send broadcast message text:"
    )


@router.message()
async def handle_broadcast_message(message: types.Message):
    user_id = message.from_user.id

    if user_id not in _pending:
        return

    _pending.remove(user_id)

    text = message.text
    chat_ids = get_chat_ids()

    sent = 0

    for chat_id in chat_ids:
        try:
            await message.bot.send_message(chat_id, text)
            sent += 1
        except Exception:
            continue

    await message.answer(f"✅ Broadcast sent to {sent} chats")