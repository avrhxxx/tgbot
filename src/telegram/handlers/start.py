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
from src.services.user.context_store import user_context_store
from src.services.user.user_profile import user_profile

logger = logging.getLogger(__name__)

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, dialog_manager: DialogManager):

    if not message.from_user:
        logger.warning("START without user")
        return

    # =====================================
    # BUILD USER CONTEXT
    # =====================================
    user_context = await context_builder.build(message.from_user)

    # STORE FOR ROUTING ENGINE
    user_context_store.set(user_context.user_id, user_context)

    logger.info(
        "Start command | user_id=%s role=%s",
        user_context.user_id,
        user_context.role,
    )

    # =====================================
    # ONBOARDING CHECK (GAME NICK)
    # =====================================
    profile = user_profile.get(user_context.user_id)

    if not profile or not profile.nickname:
        logger.info(
            "Redirecting to REGISTER | user_id=%s",
            user_context.user_id,
        )

        from src.telegram.states.register import RegisterSG

        await dialog_manager.start(
            state=RegisterSG.waiting_for_nick,
            mode=StartMode.RESET_STACK,
        )
        return

    # =====================================
    # GO TO HOME
    # =====================================
    await dialog_manager.start(
        state=HomeSG.main,
        mode=StartMode.RESET_STACK,
    )