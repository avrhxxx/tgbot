# src/api/telegram/handler.py
# GROUP: api.telegram
# DESCRIPTION: Telegram message adapter → CORE Pipeline entrypoint

from aiogram.types import Message
from src.shared.logging import get_logger
from src.core.runtime.pipeline import Pipeline

logger = get_logger("TelegramHandler")

# single shared pipeline instance (MVP)
pipeline = Pipeline()


async def handle_message(message: Message):
    """
    Entry point for all Telegram messages.
    Converts Telegram update → CORE system input.
    """
    try:
        text = message.text

        if not text:
            logger.warning("Empty message received")
            return

        logger.info(f"Incoming Telegram message: {text}")

        result = pipeline.handle(text)

        logger.info(f"Pipeline result: {result}")

        # MVP: just reply as string
        await message.answer(str(result))

    except Exception as e:
        logger.exception(f"Telegram handler error: {e}")
        await message.answer("SYSTEM ERROR")