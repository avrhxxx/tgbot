# src/webhook/setup.py
# =========================================
# GROUP: webhook
# FILE: setup.py
# DESCRIPTION:
# Idempotent webhook setup for Telegram Bot API.
# =========================================

import logging
from aiogram import Bot

logger = logging.getLogger("shadow.webhook.setup")


async def setup_webhook(bot: Bot, webhook_url: str, secret: str):
    logger.info("🔍 Checking webhook status...")

    info = await bot.get_webhook_info()
    logger.info("Current webhook URL: %s", info.url or "None")

    if info.url == webhook_url:
        logger.info("✅ Webhook already correct, skipping setup")
        return

    if info.url:
        logger.warning("⚠️ Existing webhook found, deleting...")
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("🧹 Old webhook removed")

    logger.info("🔗 Setting new webhook...")

    await bot.set_webhook(
        url=webhook_url,
        secret_token=secret,
        drop_pending_updates=True,
    )

    logger.info("✅ Webhook successfully set: %s", webhook_url)