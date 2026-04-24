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

from src.telegram.dialogs.home.state import HomeSG


logger = logging.getLogger(__name__)

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, dialog_manager: DialogManager):
    """
    Entry point of the bot.
    Routes directly into Home dialog (R3 base UI).
    """

    user_id = getattr(message.from_user, "id", None)

    if user_id is None:
        logger.warning("START received without from_user")
        return

    logger.info("Start command received | user_id=%s", user_id)

    await dialog_manager.start(
        state=HomeSG.main,
        mode=StartMode.RESET_STACK,
    )