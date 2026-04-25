# =========================================
# GROUP: telegram.handlers
# FILE: start.py
# DESCRIPTION:
# Entry point + onboarding redirect.
# FIX: always uses profile service for consistency.
# =========================================

import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from src.telegram.states.home import HomeSG
from src.telegram.permissions.context_builder import context_builder
from src.services.user.user_profile import user_profile
from src.telegram.windows.home.home import render_home

logger = logging.getLogger(__name__)

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, dialog_manager: DialogManager):

    if not message.from_user:
        logger.warning("START without user")
        return

    user = message.from_user

    user_context = await context_builder.build(user)

    logger.info(
        "Start command | user_id=%s role=%s",
        user_context.user_id,
        user_context.role,
    )

    dialog_manager.middleware_data["user_context"] = user_context

    # ensure profile exists immediately (FIX FOR HOME SYNC BUG)
    user_profile.create_or_update(
        user_id=user.id,
        nickname=user.username or user.first_name or "User",
    )

    # show home via dialog
    await dialog_manager.start(
        state=HomeSG.main,
        mode=StartMode.RESET_STACK,
    )