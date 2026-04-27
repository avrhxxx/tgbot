# =========================================
# FILE: src/handlers/start.py
# DESCRIPTION:
# Main menu (single entry button -> n8n flow)
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
    logger.info(f"🚀 START | user_id={message.from_user.id}")

    await message.answer(
        "🤖 Main Menu\n\nChoose an option:",
        reply_markup=main_menu_kb()
    )