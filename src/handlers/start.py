# =========================================
# FILE: src/handlers/start.py
# DESCRIPTION:
# Start handler (UI entrypoint only)
# =========================================

import logging
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.ui.main_menu import format_main_menu
from src.ui.keyboards.main_menu import main_menu_kb

logger = logging.getLogger(__name__)

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    user = message.from_user

    user_id = user.id if user else -1
    user_name = user.first_name if user else "unknown"

    logger.info(f"🚀 START | user_id={user_id} | user={user_name}")

    await message.answer(
        format_main_menu(user),
        reply_markup=main_menu_kb()
    )