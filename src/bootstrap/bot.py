# src/bootstrap/bot.py
# GROUP: bootstrap
# DESCRIPTION: CORE + Telegram runtime launcher (Railway entrypoint)

import asyncio
import os

from aiogram import Bot, Dispatcher

from src.adapters.telegram.webhook_server import TelegramWebhookServer
from src.shared.logging import get_logger

logger = get_logger("bootstrap")


async def main():
    logger.info("🧠 SYSTEM STARTING (CORE + TELEGRAM)")

    token = os.getenv("TELEGRAM_TOKEN")

    if not token:
        raise RuntimeError("Missing TELEGRAM_TOKEN in environment")

    bot = Bot(token=token)
    dp = Dispatcher()

    server = TelegramWebhookServer(
        bot=bot,
        dp=dp,
        secret=os.getenv("WEBHOOK_SECRET", "DUMMY_SECRET")
    )

    logger.info("🔌 Starting Telegram webhook layer...")

    await server.run()


if __name__ == "__main__":
    asyncio.run(main())