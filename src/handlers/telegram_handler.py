# src/handlers/telegram_handler.py
# GROUP: handlers
# DESCRIPTION: Main Telegram message handler (AI Wiki entrypoint)

import logging
from aiogram import types

from src.wiki.service import answer_wiki_question

logger = logging.getLogger("handlers.telegram")


async def handle_message(message: types.Message):
    user_text = message.text

    logger.info("Incoming message: %s", user_text)

    if not user_text:
        await message.answer("Send me a question.")
        return

    try:
        response = await answer_wiki_question(user_text)
        await message.answer(response)

    except Exception:
        logger.exception("Handler error")
        await message.answer("Error processing request.")