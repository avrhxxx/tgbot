# src/handlers/telegram_handler.py
# GROUP: handlers
# DESCRIPTION: Main Telegram message handler (AI Wiki entrypoint)

import logging
from aiogram import types

from src.wiki.service import answer_wiki_question

logger = logging.getLogger("handlers.telegram")

TELEGRAM_LIMIT = 4096


# =========================
# MESSAGE CHUNKER
# =========================
def split_message(text: str, limit: int = TELEGRAM_LIMIT) -> list[str]:
    if len(text) <= limit:
        return [text]

    chunks = []
    current = ""

    for line in text.split("\n"):
        if len(current) + len(line) + 1 > limit:
            chunks.append(current)
            current = line
        else:
            current += "\n" + line if current else line

    if current:
        chunks.append(current)

    return chunks


# =========================
# HANDLER
# =========================
async def handle_message(message: types.Message):
    user_text = message.text

    logger.info("Incoming message: %s", user_text)

    if not user_text:
        await message.answer("Send me a question.")
        return

    # 🔥 IMPORTANT: block all commands from AI layer
    if user_text.startswith("/"):
        return

    try:
        response = await answer_wiki_question(user_text)

        if not response:
            await message.answer("No response from AI.")
            return

        for chunk in split_message(response):
            await message.answer(chunk)

    except Exception:
        logger.exception("Handler error")
        await message.answer("Error processing request.")