# src/bootstrap/bot.py
# GROUP: bootstrap
# DESCRIPTION: Clean Telegram bot entrypoint (SAFE BOOT MODE - no AI, no Sheets, no workers)

import asyncio
import logging

from aiogram import Bot, Dispatcher, Router

from src.config.config import load_config
from src.handlers.telegram_handler import handle_message
from src.webhook.server import WebhookServer
from src.webhook.setup import setup_webhook


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bootstrap")


async def main():
    config = load_config()

    # =========================
    # TELEGRAM CORE
    # =========================
    bot = Bot(token=config.telegram.token)
    dp = Dispatcher()

    # =========================
    # ROUTING (MINIMAL)
    # =========================
    fallback_router = Router()
    fallback_router.message.register(handle_message)
    dp.include_router(fallback_router)

    # =========================
    # WEBHOOK SETUP
    # =========================
    webhook = WebhookServer(
        bot=bot,
        dp=dp,
        webhook_path="/webhook",
        secret=config.telegram.webhook_secret,
    )

    await setup_webhook(
        bot=bot,
        webhook_url=config.telegram.webhook_url,
        secret=config.telegram.webhook_secret,
    )

    logger.info("Starting CLEAN Shadow Bot (no AI / no Sheets / no workers)...")
    await webhook.run()


if __name__ == "__main__":
    asyncio.run(main())