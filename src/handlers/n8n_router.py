# =========================================
# FILE: src/handlers/n8n_router.py
# =========================================

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(F.data.startswith("menu:"))
async def menu_router(callback: CallbackQuery):
    if not callback.message:
        return

    try:
        await callback.message.edit_text("⚠️ Flow not implemented yet")
    except Exception as e:
        logger.error(f"edit failed: {e}")

    await callback.answer()