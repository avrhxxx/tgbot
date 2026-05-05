# src/bootstrap/bot.py
# GROUP: bootstrap
# DESCRIPTION: CORE + Telegram runtime launcher (Railway entrypoint)

import asyncio

from aiogram import Bot, Dispatcher

from src.adapters.telegram.webhook_server import TelegramWebhookServer
from src.config.config import load_config
from src.shared.logging import get_logger

logger = get_logger("bootstrap")


async def main():
    logger.info("🧠 SYSTEM STARTING (CORE + TELEGRAM)")

    # =========================
    # CONFIG LOAD (FAIL-FAST)
    # =========================
    config = load_config()

    telegram_cfg = config.telegram

    # HARD SAFETY CHECK (explicit, readable errors in Railway)
    if not telegram_cfg.token:
        raise RuntimeError("Missing TELEGRAM_TOKEN")

    if not telegram_cfg.webhook_secret:
        raise RuntimeError("Missing WEBHOOK_SECRET")

    if not telegram_cfg.webhook_url:
        raise RuntimeError("Missing WEBHOOK_URL")

    # =========================
    # BOT INIT
    # =========================
    bot = Bot(token=telegram_cfg.token)
    dp = Dispatcher()

    # =========================
    # WEBHOOK SERVER
    # =========================
    server = TelegramWebhookServer(
        bot=bot,
        dp=dp,
        secret=telegram_cfg.webhook_secret
    )

    logger.info("🔌 Starting Telegram webhook layer...")

    await server.run()


if __name__ == "__main__":
    asyncio.run(main())