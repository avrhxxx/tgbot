# src/bootstrap/bot.py
# GROUP: bootstrap
# DESCRIPTION: Application entrypoint for Shadow AI Wiki Bot

import asyncio
import logging

from aiogram import Bot, Dispatcher

from src.config.config import load_config
from src.webhook.server import WebhookServer
from src.webhook.setup import setup_webhook


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bootstrap")


async def main():
    config = load_config()

    # =========================
    # BOT + DISPATCHER
    # =========================
    bot = Bot(token=config.telegram.token)
    dp = Dispatcher()

    # =========================
    # WEBHOOK SERVER
    # =========================
    webhook = WebhookServer(
        bot=bot,
        dp=dp,
        webhook_path="/webhook",
        secret=config.telegram.webhook_secret
    )

    # =========================
    # SET WEBHOOK (Railway-ready)
    # =========================
    await setup_webhook(
        bot=bot,
        webhook_url=config.telegram.webhook_url,
        secret=config.telegram.webhook_secret
    )

    # =========================
    # RUN SERVER
    # =========================
    logger.info("Starting Shadow AI Wiki Bot...")
    await webhook.run()


if __name__ == "__main__":
    asyncio.run(main())