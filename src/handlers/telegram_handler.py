# src/handlers/telegram_handler.py
# GROUP: handlers
# DESCRIPTION: Minimal Telegram handler (CLEAN BOOT MODE)

from aiogram.types import Message


async def handle_message(message: Message):
    await message.answer("Bot is running (clean mode). No AI / no Sheets yet.")