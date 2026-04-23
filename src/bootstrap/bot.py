# src/bootstrap/bot.py

import asyncio
import logging

from aiogram import Bot, Dispatcher

from config.config import load_config
from src.bootstrap.app import AppContext
from src.bootstrap.middleware import AppMiddleware

from src.services.user_service import UserService
from src.services.navigation_service import NavigationService

from src.handlers.r3 import home_handler, home_router
from src.handlers.common import callback_router, text_router

from src.webhook.setup import setup_webhook
from src.webhook.server import WebhookServer


# =========================
# LOGGING
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
    # APP CONTEXT
    # =========================
    app = AppContext(config=config)

    # =========================
    # SERVICES
    # =========================
    app.services["user"] = UserService()
    app.services["nav"] = NavigationService()

    # =========================
    # SESSION ENGINE (MVP PLACEHOLDER)
    # =========================
    app.session_engine = None  # ready for next stage

    # =========================
    # MIDDLEWARE (FIXED)
    # =========================
    dp.update.outer_middleware(
        AppMiddleware(app)
    )

    # =========================
    # ROUTERS
    # =========================
    dp.include_router(home_handler.router)
    dp.include_router(home_router.router)
    dp.include_router(callback_router.router)
    dp.include_router(text_router.router)

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