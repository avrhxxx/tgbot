import logging

from aiogram import Bot

logger = logging.getLogger(__name__)


# =========================
# SET WEBHOOK (SAFE)
# =========================

async def setup_webhook(bot: Bot, webhook_url: str, secret: str):
    logger.info("Checking current webhook...")

    current = await bot.get_webhook_info()

    # =====================================
    # 🧠 IDEMPOTENCY CHECK
    # =====================================
    if current.url == webhook_url:
        logger.info("Webhook already set: %s (skipping)", webhook_url)
        return

    # =====================================
    # 🧨 ONLY DELETE IF DIFFERENT
    # =====================================
    if current.url:
        logger.info("Deleting old webhook...")
        await bot.delete_webhook(drop_pending_updates=True)

    # =====================================
    # 🚀 SET NEW WEBHOOK
    # =====================================
    logger.info("Setting new webhook...")

    await bot.set_webhook(
        url=webhook_url,
        secret_token=secret,
        drop_pending_updates=True,
    )

    logger.info("Webhook successfully set: %s", webhook_url)