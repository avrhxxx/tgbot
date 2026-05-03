# src/handlers/admin_index.py
# GROUP: handlers
# DESCRIPTION: Admin-only index creation handler

import logging

from aiogram import Router, F
from aiogram.types import Message

from src.config.config import load_config
from src.ai.intent_parser import IntentParser
from src.services.index_service import IndexService
from src.google.sheets.writer import SheetsWriter

logger = logging.getLogger("handlers.admin_index")

router = Router()

config = load_config()

intent_parser = IntentParser()


def is_admin(user_id: int) -> bool:
    return user_id in config.telegram.admin_ids


@router.message(F.text.startswith("dodaj"))
async def handle_add(message: Message):

    user_id = message.from_user.id
    text = message.text

    logger.info("📩 Admin command received | user=%s text=%s", user_id, text)

    if not is_admin(user_id):
        logger.warning("⛔ Unauthorized access attempt | user_id=%s", user_id)
        await message.answer("❌ No permission.")
        return

    logger.info("🔐 Admin verified")

    try:
        intent = intent_parser.parse(text)

        logger.info("🧠 Intent received in handler: %s", intent)

        sheets_client = SheetsWriter(message.bot["sheets_client"])
        service = IndexService(sheets_client)

        result = service.handle(intent)

        logger.info("🎯 Final result stored: %s", result)

        await message.answer(f"✅ Added: {result}")

    except Exception as e:
        logger.exception("❌ Handler failed")
        await message.answer("❌ Error while processing command.")