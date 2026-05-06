# src/adapters/telegram/handler.py
# PURPOSE: Telegram adapter layer (Stage 1 UI bridge → Core DSL pipeline)

import uuid

from src.core.runtime.pipeline import Pipeline
from src.shared.logging import get_logger

logger = get_logger("TelegramAdapter")


class TelegramHandler:

    def __init__(self):
        self.pipeline = Pipeline()

    async def handle_text(self, text: str) -> dict:
        trace_id = str(uuid.uuid4())

        logger.info(f"[trace={trace_id}] [Telegram] input: {text}")

        try:
            # =========================
            # SYSTEM COMMAND ROUTER
            # =========================
            if text.startswith("/"):
                result = self.handle_system_command(text)

                response = {
                    "status": "ok",
                    "trace_id": trace_id,
                    "result": result
                }

            else:
                # DSL ONLY PATH
                result = self.pipeline.handle(text)

                response = {
                    "status": "ok",
                    "trace_id": trace_id,
                    "result": result
                }

        except Exception as e:
            logger.error(f"[trace={trace_id}] error: {str(e)}")

            response = {
                "status": "error",
                "trace_id": trace_id,
                "error": str(e)
            }

        logger.info(f"[trace={trace_id}] [Telegram] output: {response}")
        return response

    def handle_system_command(self, text: str) -> str:

        if text == "/start":
            return "🧠 Tiles Survive bot online (Stage 1)"
        elif text == "/help":
            return "Available commands: DSL only or /start"
        else:
            return f"Unknown system command: {text}"


handler = TelegramHandler()


async def handle_telegram_text(text: str) -> dict:
    return await handler.handle_text(text)