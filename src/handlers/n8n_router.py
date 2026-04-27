# =========================================
# FILE: src/handlers/n8n_router.py
# DESCRIPTION:
# Single gateway → sends callback to n8n
# =========================================

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.n8n.client import N8NClient
from src.ui.renderer import render_edit_payload

logger = logging.getLogger(__name__)

router = Router()

n8n = N8NClient(base_url="http://n8n:5678/webhook")


@router.callback_query(F.data.startswith("menu:"))
async def menu_router(callback: CallbackQuery):
    if not callback.message:
        return

    payload = {
        "action": callback.data,
        "user_id": callback.from_user.id if callback.from_user else None,
        "chat_id": callback.message.chat.id,
        "message_id": callback.message.message_id,
    }

    data = await n8n.call("router", payload)

    if not data:
        await callback.message.edit_text("⚠️ Flow error")
        return

    text, keyboard = render_edit_payload(data)

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )

    await callback.answer()