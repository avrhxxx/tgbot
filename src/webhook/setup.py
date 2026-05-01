# src/webhook/setup.py
# GROUP: webhook
# DESCRIPTION: Telegram webhook setup (idempotent)

import logging
from aiogram import Bot

logger = logging.getLogger("webhook.setup")


async def setup_webhook(bot: Bot, webhook_url: str, secret: str):
    info = await bot.get_webhook_info()

    if info.url == webhook_url:
        logger.info("Webhook already set")
        return

    if info.url:
        await bot.delete_webhook(drop_pending_updates=True)

    await bot.set_webhook(
        url=webhook_url,
        secret_token=secret,
        drop_pending_updates=True,
    )

    logger.info("Webhook set: %s", webhook_url)