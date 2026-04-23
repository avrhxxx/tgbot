# src/bootstrap/bot.py

import asyncio
import logging

from aiogram import Bot, Dispatcher

from config.config import load_config
from src.bootstrap.app import AppContext
from src.bootstrap.middleware import AppMiddleware

from src.services.user_service import UserService

from src.ui.screen_registry import ScreenRegistry
from src.ui.bootstrap_screens import register_screens
from src.ui.screen_middleware import ScreenMiddlewareManager, InjectUserMiddleware
from src.ui.screen_engine import ScreenEngine
from src.ui.screen_router import ScreenRouter

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


async def main():
    logger.info("Starting Shadow Bot...")

    config = load_config()

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    # =========================
    # APP CONTEXT
    # =========================
    app = AppContext(config=config)

    # =========================
    # SERVICES
    # =========================
    app.services["user"] = UserService()

    # =========================
    # SCREEN SYSTEM (FULL PIPELINE)
    # =========================

    # 1. Registry
    registry = ScreenRegistry()
    register_screens(registry)

    # 2. Middleware
    middleware = ScreenMiddlewareManager()
    middleware.add(InjectUserMiddleware())

    # 3. Engine
    engine = ScreenEngine(registry, middleware)

    # 4. Router (IMPORTANT: ENGINE not registry)
    router = ScreenRouter(engine)

    # =========================
    # ATTACH TO APP CONTEXT
    # =========================
    app.ui["registry"] = registry
    app.ui["engine"] = engine
    app.ui["router"] = router

    # =========================
    # MIDDLEWARE (GLOBAL APP)
    # =========================
    dp.update.outer_middleware(AppMiddleware(app))

    # =========================
    # ROUTERS
    # =========================
    dp.include_router(callback_router.router)
    dp.include_router(text_router.router)

    # =========================
    # WEBHOOK
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


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Shutdown signal received")