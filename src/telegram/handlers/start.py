# =========================================
# GROUP: telegram.handlers
# FILE: start.py
# DESCRIPTION:
# Entry point of the bot.
# Routes user into Home dialog (R3 base UI).
# =========================================

import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from src.telegram.states.home import HomeSG
from src.telegram.permissions.context_builder import context_builder

logger = logging.getLogger(__name__)

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, dialog_manager: DialogManager):

    if not message.from_user:
        logger.warning("START without user")
        return

    # 🔥 BUILD USER CONTEXT
    user_context = await context_builder.build(message.from_user)

    logger.info(
        "Start command | user_id=%s role=%s",
        user_context.user_id,
        user_context.role,
    )

    # store context inside dialog_manager for later engine access
    dialog_manager.middleware_data["user_context"] = user_context

    await dialog_manager.start(
        state=HomeSG.main,
        mode=StartMode.RESET_STACK,
    )