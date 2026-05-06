from src.core.runtime.pipeline import Pipeline
from src.shared.logging import get_logger

logger = get_logger("TelegramAdapter")


class TelegramHandler:

    def __init__(self):
        self.pipeline = Pipeline()

    async def handle_text(self, text: str) -> str:
        logger.info(f"[Telegram] input: {text}")

        # =========================
        # SYSTEM COMMAND ROUTER
        # =========================
        if text.startswith("/"):
            result = self.handle_system_command(text)
        else:
            # DSL ONLY PATH
            result = self.pipeline.handle(text)

        logger.info(f"[Telegram] output: {result}")
        return str(result)

    def handle_system_command(self, text: str) -> str:
        """
        System layer commands (/start, /help etc.)
        MUST NOT touch CORE DSL
        """

        if text == "/start":
            return "🧠 Tiles Survive bot online (Stage 1)"
        elif text == "/help":
            return "Available commands: DSL only or /start"
        else:
            return f"Unknown system command: {text}"


handler = TelegramHandler()


async def handle_telegram_text(text: str) -> str:
    return await handler.handle_text(text)