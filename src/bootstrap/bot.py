# src/bootstrap/bot.py
# GROUP: bootstrap
# DESCRIPTION: Clean Telegram bot entrypoint (SAFE BOOT MODE + Google Auth + Sheets + AI warmup)

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

# 🔥 AI warmup import
from src.ai.gemini import gemini_client


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bootstrap")


async def main():

    # =========================
    # CONFIG
    # =========================
    config = load_config()

    # =========================
    # 🤖 AI WARMUP (CRITICAL)
    # =========================
    logger.info("🧠 Warming up Vertex AI (Gemini)...")

    try:
        gemini_client.generate("ping")
        logger.info("✅ Vertex AI warmup successful")
    except Exception as e:
        logger.error("❌ Vertex AI warmup failed: %s", e)
        raise RuntimeError("AI layer is not available. Stopping boot.") from e

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
    # 📊 GOOGLE SHEETS INIT
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
    # TELEGRAM BOT
    # =========================
    bot = Bot(token=config.telegram.token)
    dp = Dispatcher()

    # context injection (safe)
    bot.__dict__["sheets_client"] = sheets_client

    # =========================
    # ROUTING
    # =========================
    dp.include_router(admin_index_router)

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

    # =========================
    # FINAL BOOT STATUS
    # =========================
    logger.info("🚀 Shadow Bot starting...")

    logger.info(
        "📦 SYSTEM READY STATE | AI=%s | SHEETS=%s | AUTH=%s",
        "OK",
        "OK" if sheets_client else "DISABLED",
        "OK" if creds else "FAILED",
    )

    await webhook.run()


if __name__ == "__main__":
    asyncio.run(main())