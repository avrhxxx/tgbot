# =========================================
# FILE: src/handlers/n8n_bridge.py
# DESCRIPTION:
# Thin bridge → Telegram → n8n → Telegram
# =========================================

import logging
import httpx

from aiogram import Router
from aiogram.types import CallbackQuery

logger = logging.getLogger(__name__)

router = Router()


N8N_URL = "http://localhost:5678/webhook/bot-router"  # później config


@router.callback_query(lambda c: c.data.startswith("flow:"))
async def handle_flow(callback: CallbackQuery):
    user = callback.from_user

    payload = {
        "flow": callback.data,
        "user_id": user.id if user else None,
        "chat_id": callback.message.chat.id if callback.message else None,
        "message_id": callback.message.message_id if callback.message else None,
    }

    logger.info(f"➡️ SEND TO N8N | {payload}")

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(N8N_URL, json=payload)
            data = resp.json()

        text = data.get("text", "No response from flow")
        keyboard = data.get("keyboard")

        await callback.message.edit_text(text)

    except Exception as e:
        logger.error(f"❌ N8N ERROR: {e}")
        await callback.message.answer("Flow error")

    await callback.answer()