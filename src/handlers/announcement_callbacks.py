# =========================================
# FILE: src/handlers/announcement_callbacks.py
# DESCRIPTION:
# Handles inline actions for announcement flow
# =========================================

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.engine.flow_state import get_state, set_step

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "announce_send")
async def send_announcement(callback: CallbackQuery):
    user_id = callback.from_user.id
    state = get_state(user_id)

    data = state["data"]

    text = (
        f"📣 ANNOUNCEMENT\n\n"
        f"{data.get('title')}\n\n"
        f"{data.get('content')}"
    )

    if callback.message:
        await callback.message.answer(text)

    await callback.answer("Sent ✔")


@router.callback_query(F.data == "announce_edit_title")
async def edit_title(callback: CallbackQuery):
    user_id = callback.from_user.id
    set_step(user_id, "title")

    if callback.message:
        await callback.message.answer("📝 Enter title again")

    await callback.answer()


@router.callback_query(F.data == "announce_edit_content")
async def edit_content(callback: CallbackQuery):
    user_id = callback.from_user.id
    set_step(user_id, "content")

    if callback.message:
        await callback.message.answer("✍️ Write message again")

    await callback.answer()