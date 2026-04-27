# =========================================
# FILE: src/handlers/start.py
# DESCRIPTION:
# Main menu (n8n MVP safe version)
# =========================================

import logging
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

logger = logging.getLogger(__name__)

router = Router()


def main_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📣 Announcements",
                    callback_data="flow:announcement"
                )
            ]
        ]
    )


@router.message(CommandStart())
async def start_handler(message: Message):
    user = message.from_user

    user_id = user.id if user else -1
    user_name = user.full_name if user else "unknown"

    logger.info(f"🚀 START | user_id={user_id} | user={user_name}")

    await message.answer(
        "🤖 Main Menu\n\nChoose an option:",
        reply_markup=main_menu_kb()
    )