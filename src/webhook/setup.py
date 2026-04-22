import logging

from aiogram import Bot

logger = logging.getLogger(__name__)


# =========================
# SET WEBHOOK
# =========================

async def setup_webhook(bot: Bot, webhook_url: str, secret: str):
    logger.info("Deleting old webhook...")

    await bot.delete_webhook(drop_pending_updates=True)

    logger.info("Setting new webhook...")

    await bot.set_webhook(
        url=webhook_url,
        secret_token=secret,
    )

    logger.info("Webhook successfully set: %s", webhook_url)