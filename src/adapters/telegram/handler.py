# src/adapters/telegram/handler.py
# GROUP: adapters.telegram
# DESCRIPTION: Telegram → CORE bridge (no business logic)

from src.core.runtime.pipeline import Pipeline
from src.shared.logging import get_logger

logger = get_logger("TelegramAdapter")


class TelegramHandler:
    """
    Adapter layer:
    ONLY responsibility = pass data into CORE pipeline
    """

    def __init__(self):
        self.pipeline = Pipeline()

    async def handle_text(self, text: str) -> str:
        """
        Entry point for Telegram messages
        """

        logger.info(f"[Telegram] input: {text}")

        # CORE is sync → safe call (for now)
        result = self.pipeline.handle(text)

        logger.info(f"[Telegram] output: {result}")

        return str(result)


# singleton instance (safe for now, replace later with DI container)
handler = TelegramHandler()


async def handle_telegram_text(text: str) -> str:
    return await handler.handle_text(text)