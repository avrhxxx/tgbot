# src/handlers/admin_index.py
# GROUP: handlers
# DESCRIPTION: Admin-only index creation handler (SAFE DI + runtime guards)

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


# =========================
# ADMIN CHECK
# =========================
def is_admin(user_id: int) -> bool:
    return user_id in getattr(config.telegram, "admin_ids", [])


# =========================
# HANDLER
# =========================
@router.message(F.text.startswith("dodaj"))
async def handle_add(message: Message):

    if not message.from_user:
        return

    user_id = message.from_user.id
    text = message.text or ""

    logger.info("📩 Admin command received | user=%s | text=%s", user_id, text)

    # -------------------------
    # AUTH CHECK
    # -------------------------
    if not is_admin(user_id):
        logger.warning("⛔ Unauthorized access attempt | user_id=%s", user_id)
        await message.answer("❌ No permission.")
        return

    logger.info("🔐 Admin verified")

    try:
        # -------------------------
        # INTENT PARSE
        # -------------------------
        intent = intent_parser.parse(str(text))

        logger.info("🧠 Intent parsed | %s", intent)

        # -------------------------
        # SAFE SHEETS CLIENT ACCESS
        # -------------------------
        sheets_client = message.bot.get("sheets_client")

        if not sheets_client:
            logger.error("❌ Sheets client not found in bot context")
            await message.answer("❌ Sheets not initialized.")
            return

        # -------------------------
        # SERVICE LAYER
        # -------------------------
        writer = SheetsWriter(sheets_client)
        service = IndexService(writer)

        result = service.handle(intent)

        logger.info("🎯 Index stored successfully | %s", result)

        await message.answer(f"✅ Added: {result}")

    except Exception:
        logger.exception("❌ Handler failed")
        await message.answer("❌ Error while processing command.")