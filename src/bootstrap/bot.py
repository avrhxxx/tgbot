# src/bootstrap/bot.py

import asyncio
import logging

from aiogram import Bot, Dispatcher

from config.config import load_config
from src.bootstrap.app import AppContext

from src.handlers.r3 import home_handler
from src.handlers.common import callback_router

from src.webhook.setup import setup_webhook
from src.webhook.server import WebhookServer


# =========================
# LOGGING (STANDARD PYTHON)
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(filename)s:%(lineno)d [%(levelname)s] %(asctime)s - %(message)s",
)

logger = logging.getLogger("shadow.bot")


# =========================
# MAIN ENTRYPOINT
# =========================
async def main():
    logger.info("Starting Shadow Bot...")

    # =========================
    # CONFIG
    # =========================
    config = load_config()

    # =========================
    # BOT CORE
    # =========================
    bot = Bot(
        token=config.tg_bot.token,
        parse_mode="HTML",
    )

    dp = Dispatcher()

    # =========================
    # APP CONTEXT (RUNTIME CORE)
    # =========================
    app = AppContext(config=config)

    # =========================
    # ATTACH SERVICES (PLACEHOLDERS FOR NOW)
    # =========================
    app.services["session"] = None  # will be injected in next step

    # =========================
    # ROUTERS (ROLE-BASED SYSTEM)
    # =========================
    dp.include_router(home_handler.router)
    dp.include_router(callback_router.router)

    # =========================
    # WEBHOOK SETUP
    # =========================
    await setup_webhook(
        bot=bot,
        webhook_url=config.tg_bot.webhook_url,
        secret=config.tg_bot.webhook_secret,
    )

    server = WebhookServer(
        bot=bot,
        dp=dp,
        webhook_path="/webhook",
        secret=config.tg_bot.webhook_secret,
    )

    try:
        logger.info("Webhook server starting...")
        await server.run(port=8080)

    finally:
        await bot.session.close()
        logger.info("Bot stopped safely")


# =========================
# ENTRYPOINT
# =========================
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Shutdown signal received")