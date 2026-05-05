# src/bootstrap/bot.py
# GROUP: bootstrap
# DESCRIPTION: Application entrypoint for Shadow AI System

import asyncio
import logging

from aiogram import Bot, Dispatcher, Router

from src.config.config import load_config
from src.webhook.server import WebhookServer
from src.webhook.setup import setup_webhook

# CORE IMPORT (pipeline smoke test stays optional)
from src.core.runtime.pipeline import Pipeline

# TELEGRAM HANDLER
from src.api.telegram.handler import handle_message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bootstrap")


async def main():
    config = load_config()

    bot = Bot(token=config.telegram.token)
    dp = Dispatcher()

    # =========================
    # TELEGRAM ROUTER
    # =========================
    fallback_router = Router()

    fallback_router.message.register(handle_message)
    dp.include_router(fallback_router)

    # =========================
    # CORE SMOKE TEST (OPTIONAL)
    # =========================
    pipeline = Pipeline()

    logger.info("Running CORE smoke test...")
    test_result = pipeline.handle('create hero "TestHero"')
    logger.info(f"CORE test result: {test_result}")

    # =========================
    # WEBHOOK SETUP
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

    logger.info("System fully started (Telegram + CORE connected)")
    await webhook.run()


if __name__ == "__main__":
    asyncio.run(main())