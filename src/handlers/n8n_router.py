# =========================================
# FILE: src/handlers/n8n_router.py
# DESCRIPTION:
# N8N webhook bridge (clean version)
# =========================================

import logging
from aiogram import Router
from aiogram.types import CallbackQuery

router = Router()
logger = logging.getLogger(__name__)


async def send_from_n8n(callback: CallbackQuery, data: dict):
    msg = callback.message

    if not msg:
        await callback.answer("No message context")
        return

    text = data.get("text", "No response from flow")

    try:
        await msg.edit_text(text)
    except Exception:
        await msg.answer("Flow error")

    await callback.answer()