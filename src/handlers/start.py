# =========================================
# FILE: src/handlers/start.py
# =========================================

import logging
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from aiogram_dialog import DialogManager
from aiogram_dialog import StartMode

from src.dialogs.main_menu.states import MainMenuSG

router = Router()

logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def start_handler(message: Message, dialog_manager: DialogManager):
    logger.info(f"🚀 START | user_id={message.from_user.id}")

    await dialog_manager.start(
        MainMenuSG.main,
        mode=StartMode.RESET_STACK,
    )