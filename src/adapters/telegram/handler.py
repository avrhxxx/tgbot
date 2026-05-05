# src/adapters/telegram/handler.py
# GROUP: adapters.telegram
# DESCRIPTION: Telegram → CORE bridge (no business logic)

from src.core.runtime.pipeline import Pipeline
from src.shared.logging import get_logger

logger = get_logger("TelegramAdapter")

pipeline = Pipeline()


async def handle_telegram_text(text: str) -> str:
    """
    ONLY responsibility:
    pass Telegram message into CORE system
    """
    logger.info(f"[Telegram] input: {text}")

    result = pipeline.handle(text)

    logger.info(f"[Telegram] output: {result}")

    return str(result)