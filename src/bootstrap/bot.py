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
    logger.info("🚀 Shadow Bot starting...")

    # =========================
    # LOAD CONFIG
    # =========================
    logger.info("📦 Loading config...")
    config = load_config()
    logger.info("✅ Config loaded")

    # =========================
    # INIT CORE
    # =========================
    logger.info("🤖 Initializing bot...")
    bot = create_bot()

    logger.info("📡 Initializing dispatcher...")
    dp = create_dispatcher()

    logger.info("✅ Core initialized (bot + dispatcher)")

    # =========================
    # SETUP WEBHOOK
    # =========================
    logger.info("🔗 Setting up webhook...")
    await setup_webhook(
        bot=bot,
        webhook_url=config.tg_bot.webhook_url,
        secret=config.tg_bot.webhook_secret,
    )
    logger.info("✅ Webhook ready")

    # =========================
    # START SERVER
    # =========================
    logger.info("🌐 Starting webhook server...")

    server = WebhookServer(
        bot=bot,
        dp=dp,
        webhook_path="/webhook",
        secret=config.tg_bot.webhook_secret,
    )

    logger.info("🟢 Server running on 0.0.0.0:8080")

    await server.run(host="0.0.0.0", port=8080)


if __name__ == "__main__":
    asyncio.run(main())