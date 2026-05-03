# src/bootstrap/bot.py
# GROUP: bootstrap
# DESCRIPTION: Application entrypoint for Shadow AI Wiki Bot

import asyncio
import logging

from aiogram import Bot, Dispatcher, Router

from src.config.config import load_config
from src.handlers.telegram_handler import handle_message
from src.handlers.admin_learn import router as learn_router
from src.webhook.server import WebhookServer
from src.webhook.setup import setup_webhook

# 🔥 NEW IMPORTS
from src.google.sheets.client import GoogleSheetsClient
from src.wiki.workers.source_sync_worker import SourceSyncWorker


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bootstrap")


async def main():
    config = load_config()

    bot = Bot(token=config.telegram.token)
    dp = Dispatcher()

    # =========================
    # ROUTERS (ORDER MATTERS)
    # =========================
    dp.include_router(learn_router)

    fallback_router = Router()
    fallback_router.message.register(handle_message)
    dp.include_router(fallback_router)

    # =========================
    # 🔥 INIT INFRA
    # =========================
    sheets = GoogleSheetsClient()

    if sheets.sheet_id:
        logger.info("Initializing Google Sheets structure...")
        sheets.ensure_structure()
    else:
        logger.warning("Sheets disabled (no SHEET_ID)")

    # =========================
    # 🔥 WORKER (BACKGROUND)
    # =========================
    worker = SourceSyncWorker(sheets_client=sheets)

    asyncio.create_task(worker.run())

    logger.info("Source sync worker started")

    # =========================
    # WEBHOOK
    # =========================
    webhook = WebhookServer(
        bot=bot,
        dp=dp,
        webhook_path="/webhook",
        secret=config.telegram.webhook_secret
    )

    await setup_webhook(
        bot=bot,
        webhook_url=config.telegram.webhook_url,
        secret=config.telegram.webhook_secret
    )

    logger.info("Starting Shadow AI Wiki Bot...")
    await webhook.run()


if __name__ == "__main__":
    asyncio.run(main())