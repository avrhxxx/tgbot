# src/handlers/admin_index.py
# GROUP: handlers
# DESCRIPTION: Admin AI terminal (DSL → Command → Engine → Execution)

import logging

from aiogram import Router, F
from aiogram.types import Message

from src.config.config import load_config
from src.ai.intent_parser import IntentParser
from src.core.commands.command_model import Command
from src.core.commands.command_router import CommandRouter

from src.core.entity_engine.entity_engine import EntityEngine
from src.services.index_service import IndexService

logger = logging.getLogger("handlers.admin_index")

router = Router()

config = load_config()

# =========================
# CORE SYSTEM INIT (SINGLETONS)
# =========================
intent_parser = IntentParser()
entity_engine = EntityEngine()
index_service = IndexService()
command_router = CommandRouter(entity_engine, index_service)


def is_admin(user_id: int) -> bool:
    return user_id in config.telegram.admin_ids


@router.message()
async def handle_admin(message: Message):

    if not message.from_user:
        return

    user_id = message.from_user.id
    text = message.text or ""

    logger.info("📩 Admin command | user=%s | text=%s", user_id, text)

    # =========================
    # AUTH
    # =========================
    if not is_admin(user_id):
        await message.answer("❌ No permission.")
        return

    try:
        # =========================
        # 1. PARSE DSL → DICT
        # =========================
        intent_data = intent_parser.parse(text)

        # =========================
        # 2. MAP → COMMAND (AST)
        # =========================
        command = Command(
            action=intent_data.get("action"),
            entity=intent_data.get("entity"),
            target=intent_data.get("name"),
            field=intent_data.get("field"),
            value=intent_data.get("value"),
            context={
                "target": intent_data.get("target")
            }
        )

        logger.info("🧠 Command built | %s", command)

        # =========================
        # 3. EXECUTION PIPELINE
        # =========================
        result = command_router.route(command)

        # =========================
        # RESPONSE
        # =========================
        await message.answer(f"✅ {result}")

    except Exception as e:
        logger.exception("❌ Admin handler failed")
        await message.answer(f"❌ Error: {str(e)}")