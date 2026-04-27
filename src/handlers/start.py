# =========================================
# FILE: src/handlers/start.py
# DESCRIPTION:
# Bot entry point → shows main menu only
# =========================================

import logging

from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.utils.access import can_use_panel

logger = logging.getLogger(__name__)

router = Router()


# =========================
# MENU KEYBOARD
# =========================

main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📣 Create announcement")],
    ],
    resize_keyboard=True
)


# =========================
# START HANDLER
# =========================

@router.message(CommandStart())
async def start_handler(message: types.Message):
    user = message.from_user

    if user is None:
        logger.warning("START: missing user")
        return

    if not can_use_panel(user.id):
        logger.info(f"START: access denied user_id={user.id}")
        return

    logger.info(f"START: menu shown user_id={user.id}")

    await message.answer(
        " ",
        reply_markup=main_menu_kb
    )