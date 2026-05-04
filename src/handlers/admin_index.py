# src/handlers/admin_index.py
# GROUP: handlers
# DESCRIPTION: Admin-only index + knowledge + docs creation handler (Sheets + Firestore + Docs)

import logging

from aiogram import Router, F
from aiogram.types import Message

from src.config.config import load_config
from src.ai.intent_parser import IntentParser
from src.services.index_service import IndexService
from src.services.knowledge_service import KnowledgeService
from src.google.sheets.writer import SheetsWriter

logger = logging.getLogger("handlers.admin_index")

router = Router()

config = load_config()
intent_parser = IntentParser()


def is_admin(user_id: int) -> bool:
    return user_id in config.telegram.admin_ids


@router.message(F.text.startswith("dodaj"))
async def handle_add(message: Message):

    if not message.from_user:
        return

    user_id = message.from_user.id
    text = message.text or ""

    logger.info("📩 Admin command received | user=%s | text=%s", user_id, text)

    # =========================
    # AUTH CHECK
    # =========================
    if not is_admin(user_id):
        logger.warning("⛔ Unauthorized access attempt | user_id=%s", user_id)
        await message.answer("❌ No permission.")
        return

    logger.info("🔐 Admin verified")

    try:
        # =========================
        # INTENT PARSE
        # =========================
        intent = intent_parser.parse(text)

        logger.info("🧠 Intent parsed | %s", intent)

        # =========================
        # DEPENDENCIES (BOT CONTEXT - SINGLETON SAFE)
        # =========================
        bot = message.bot

        sheets_client = getattr(bot, "sheets_client", None)
        _ = getattr(bot, "drive_client", None)  # reserved (unused but kept for DI consistency)
        docs_service = getattr(bot, "docs_service", None)

        if not sheets_client:
            logger.error("❌ Sheets client missing in bot context")
            await message.answer("❌ Sheets not initialized.")
            return

        if not docs_service:
            logger.error("❌ Docs service missing in bot context")
            await message.answer("❌ Docs not initialized.")
            return

        writer = SheetsWriter(sheets_client)

        index_service = IndexService(writer)
        knowledge_service = KnowledgeService()

        # =========================
        # ROUTING LAYER
        # =========================
        action = intent.get("action")

        # -------------------------
        # INDEX SYSTEM (Sheets)
        # -------------------------
        if action == "add_definition":
            result = index_service.handle(intent)

        # -------------------------
        # KNOWLEDGE SYSTEM (Firestore)
        # -------------------------
        elif action == "add_knowledge":
            result = await knowledge_service.create_or_update(
                intent["object"],
                intent["name"],
                intent.get("knowledge", intent.get("context", {})),
            )

        # -------------------------
        # DOCS SYSTEM (OLD)
        # -------------------------
        elif action == "create_hero_document":
            result = await docs_service.create_hero_document(
                intent["name"]
            )

        # -------------------------
        # DOCS SYSTEM (NEW GENERIC)
        # -------------------------
        elif action == "create_document":

            obj = intent.get("object")

            if obj == "hero":
                result = await docs_service.create_hero_document(
                    intent["name"]
                )
            else:
                logger.error("❌ Unsupported document object: %s", obj)
                await message.answer(f"❌ Unsupported document type: {obj}")
                return

        else:
            logger.error("❌ Unsupported action: %s", action)
            await message.answer(f"❌ Unsupported action: {action}")
            return

        # =========================
        # RESPONSE
        # =========================
        logger.info("🎯 Operation successful | %s", result)
        await message.answer(f"✅ Success: {result}")

    except Exception:
        logger.exception("❌ Handler failed")
        await message.answer("❌ Error while processing command.")