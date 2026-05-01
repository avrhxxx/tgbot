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

    bot = Bot(token=config.bot.token)
    dp = Dispatcher()

    webhook = WebhookServer(
        bot=bot,
        dp=dp,
        webhook_path="/webhook",
        secret="shadow_secret"
    )

    await setup_webhook(
        bot=bot,
        webhook_url="https://YOUR_DOMAIN/webhook",
        secret="shadow_secret"
    )

    await webhook.run()


if __name__ == "__main__":
    asyncio.run(main())