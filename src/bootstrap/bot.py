# src/bootstrap/bot.py
# =========================================
# GROUP: bootstrap
# FILE: bot.py
# DESCRIPTION:
# Application entrypoint.
# Initializes bot, dispatcher, and webhook server.
# =========================================

import asyncio
import logging

from src.factory.bot import create_bot
from src.factory.dispatcher import create_dispatcher
from src.webhook.server import WebhookServer
from src.webhook.setup import setup_webhook
from src.config.config import load_config


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)


async def main():
    logger.info("Starting Shadow Bot...")

    # =========================
    # LOAD CONFIG
    # =========================
    config = load_config()

    # =========================
    # INIT CORE
    # =========================
    bot = create_bot()
    dp = create_dispatcher()

    # =========================
    # SETUP WEBHOOK
    # =========================
    await setup_webhook(
        bot=bot,
        webhook_url=config.tg_bot.webhook_url,
        secret=config.tg_bot.webhook_secret,
    )

    # =========================
    # START SERVER
    # =========================
    server = WebhookServer(
        bot=bot,
        dp=dp,
        webhook_path="/webhook",
        secret=config.tg_bot.webhook_secret,
    )

    logger.info("Starting webhook server...")

    await server.run(host="0.0.0.0", port=8080)


if __name__ == "__main__":
    asyncio.run(main())