# src/bootstrap/bot.py
# GROUP: bootstrap
# DESCRIPTION: CORE + Telegram runtime launcher (Railway entrypoint)

import asyncio
import logging

from aiogram import Bot, Dispatcher

from src.adapters.telegram.webhook_server import TelegramWebhookServer
from src.shared.logging import get_logger

logger = get_logger("bootstrap")


async def main():
    logger.info("🧠 SYSTEM STARTING (CORE + TELEGRAM)")

    bot = Bot(token="DUMMY")  # Railway env later
    dp = Dispatcher()

    server = TelegramWebhookServer(
        bot=bot,
        dp=dp,
        secret="DUMMY_SECRET"
    )

    logger.info("🔌 Starting Telegram webhook layer...")

    await server.run()


if __name__ == "__main__":
    asyncio.run(main())