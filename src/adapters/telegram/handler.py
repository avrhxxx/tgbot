# src/adapters/telegram/handler.py

from src.core.runtime.pipeline import Pipeline
from src.shared.logging import get_logger

logger = get_logger("TelegramAdapter")


class TelegramHandler:

    def __init__(self):
        self.pipeline = Pipeline()

    async def handle_text(self, text: str) -> str:

        logger.info(f"[Telegram] input: {text}")

        result = self.pipeline.handle(text)

        logger.info(f"[Telegram] output: {result}")

        return str(result)


handler = TelegramHandler()


async def handle_telegram_text(text: str) -> str:
    return await handler.handle_text(text)