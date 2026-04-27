# =========================================
# FILE: src/handlers/n8n_router.py
# DESCRIPTION:
# Thin shell -> n8n webhook bridge (safe version)
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

    message = callback.message

    if not user or not message:
        logger.warning("⚠️ Invalid callback payload (missing user/message)")
        return await callback.answer("Error")

    payload = {
        "user_id": user.id,
        "chat_id": message.chat.id,
        "message_id": message.message_id,
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