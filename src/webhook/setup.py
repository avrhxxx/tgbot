# src/webhook/setup.py

import logging

from aiogram import Bot

logger = logging.getLogger("shadow.webhook.setup")


# =========================
# SETUP WEBHOOK (IDEMPOTENT)
# =========================
async def setup_webhook(bot: Bot, webhook_url: str, secret: str):
    logger.info("Checking webhook status...")

    info = await bot.get_webhook_info()

    if info.url == webhook_url:
        logger.info("Webhook already set, skipping")
        return

    if info.url:
        logger.info("Deleting existing webhook...")
        await bot.delete_webhook(drop_pending_updates=True)

    logger.info("Setting webhook...")

    await bot.set_webhook(
        url=webhook_url,
        secret_token=secret,
        drop_pending_updates=True,
    )

    logger.info("Webhook set successfully: %s", webhook_url)