# =========================================
# FILE: src/handlers/n8n_router.py
# DESCRIPTION:
# Callback bridge -> n8n webhook (single flow MVP)
# =========================================

import logging
import httpx

from aiogram import Router
from aiogram.types import CallbackQuery

logger = logging.getLogger(__name__)

router = Router()

N8N_WEBHOOK_URL = "http://localhost:5678/webhook/telegram-router"


@router.callback_query()
async def n8n_callback_router(callback: CallbackQuery):
    user = callback.from_user

    payload = {
        "user_id": user.id,
        "chat_id": callback.message.chat.id,
        "message_id": callback.message.message_id,
        "callback_data": callback.data,
        "user_name": user.full_name,
    }

    logger.info(f"📡 N8N ROUTE | {payload}")

    try:
        async with httpx.AsyncClient() as client:
            await client.post(N8N_WEBHOOK_URL, json=payload)
    except Exception as e:
        logger.error(f"❌ N8N webhook error: {e}")

    await callback.answer("Processing...")