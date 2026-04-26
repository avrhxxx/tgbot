# src/handlers/broadcast.py
# DESCRIPTION:
# Simple broadcast flow (FSM-less MVP version).

from aiogram import Router, types

from src.utils.access import is_mod, get_chat_ids

router = Router()

_pending: set[int] = set()


@router.message(lambda m: m.text == "/broadcast")
async def start_broadcast(message: types.Message):
    user = message.from_user

    if user is None:
        await message.answer("❌ Unable to identify user.")
        return

    user_id = user.id

    if not is_mod(user_id):
        await message.answer("❌ No access.")
        return

    _pending.add(user_id)

    await message.answer("📣 Send broadcast message text:")


@router.message()
async def handle_broadcast_message(message: types.Message):
    user = message.from_user

    if user is None:
        return

    user_id = user.id

    if user_id not in _pending:
        return

    _pending.remove(user_id)

    text = message.text
    if not text:
        await message.answer("❌ Empty message. Broadcast cancelled.")
        return

    bot = message.bot
    if bot is None:
        await message.answer("❌ Internal error (bot unavailable).")
        return

    chat_ids = get_chat_ids()

    sent = 0

    for chat_id in chat_ids:
        try:
            await bot.send_message(chat_id, text)
            sent += 1
        except Exception:
            continue

    await message.answer(f"✅ Broadcast sent to {sent} chats")