# =========================================
# FILE: src/flows/announcement_flow.py
# DESCRIPTION:
# N8N-style announcement flow (replacement for Dialog)
# =========================================

import logging
from aiogram import types

from src.engine.flow_state import (
    get_state,
    set_flow,
    set_step,
    set_data
)

logger = logging.getLogger(__name__)

FLOW_NAME = "announcement"


async def start_flow(message: types.Message):
    user = message.from_user
    if user is None:
        return

    set_flow(user.id, FLOW_NAME)
    set_step(user.id, "title")

    await message.answer("📝 Enter title")


async def handle_message(message: types.Message):
    user = message.from_user
    if user is None:
        return False

    user_id = user.id
    state = get_state(user_id)

    if state["flow"] != FLOW_NAME:
        return False

    step = state["step"]
    text = (message.text or "").strip()

    # TITLE
    if step == "title":
        set_data(user_id, "title", text)
        set_step(user_id, "content")

        await message.answer("✍️ Write message")
        return True

    # CONTENT
    if step == "content":
        set_data(user_id, "content", text)
        set_step(user_id, "preview")

        data = get_state(user_id)["data"]

        preview = (
            f"📣 ANNOUNCEMENT\n\n"
            f"Title: {data.get('title')}\n"
            f"Content: {data.get('content')}\n\n"
            f"Send?"
        )

        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="🚀 Send", callback_data="announce_send")],
            [types.InlineKeyboardButton(text="✏ Edit title", callback_data="announce_edit_title")],
            [types.InlineKeyboardButton(text="✏ Edit content", callback_data="announce_edit_content")],
        ])

        await message.answer(preview, reply_markup=keyboard)
        return True

    return False