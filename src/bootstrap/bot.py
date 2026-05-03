# src/bootstrap/bot.py
# GROUP: bootstrap
# DESCRIPTION: Clean Telegram bot entrypoint (SAFE BOOT MODE + Google Auth + Sheets Bootstrap)

import asyncio
import logging

from aiogram import Bot, Dispatcher, Router

from src.config.config import load_config
from src.handlers.telegram_handler import handle_message
from src.handlers.admin_index import router as admin_index_router
from src.webhook.server import WebhookServer
from src.webhook.setup import setup_webhook

from src.google.auth import load_google_credentials
from src.google.sheets.client import GoogleSheetsClient
from src.google.sheets.bootstrap import SheetsBootstrap


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bootstrap")


async def main():
    config = load_config()

    # =========================
    # 🔐 GOOGLE AUTH
    # =========================
    logger.info("🔐 Checking Google authentication...")

    try:
        creds = load_google_credentials()

        logger.info("✅ Google auth initialized successfully")
        logger.info("🔑 Auth type: %s", type(creds).__name__)

    except Exception as e:
        logger.error("❌ Google auth failed: %s", e)
        creds = None

    # =========================
    # 📊 GOOGLE SHEETS BOOTSTRAP
    # =========================
    sheets_client = None

    if creds:
        try:
            logger.info("📊 Initializing Google Sheets client...")

            sheets_client = GoogleSheetsClient(credentials=creds)

            bootstrap = SheetsBootstrap(client=sheets_client)

            logger.info("📊 Running Sheets schema bootstrap...")

            bootstrap.ensure()

            logger.info("✅ Sheets bootstrap completed successfully")

        except Exception as e:
            logger.error("❌ Sheets bootstrap failed: %s", e)

    else:
        logger.warning("⚠️ Sheets skipped (no valid Google credentials)")

    # =========================
    # TELEGRAM CORE
    # =========================
    bot = Bot(token=config.telegram.token)
    dp = Dispatcher()

    # =========================
    # ROUTING (IMPORTANT ORDER)
    # =========================

    # 1. Admin / index engine FIRST (highest priority)
    dp.include_router(admin_index_router)

    # 2. Fallback handler LAST
    fallback_router = Router()
    fallback_router.message.register(handle_message)
    dp.include_router(fallback_router)

    # =========================
    # WEBHOOK
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

    logger.info("🚀 Starting CLEAN Shadow Bot (auth + sheets + webhook)...")
    await webhook.run()


if __name__ == "__main__":
    asyncio.run(main())