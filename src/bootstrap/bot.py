# src/bootstrap/bot.py

"""
Shadow Bot bootstrap entrypoint.
"""

import asyncio
import logging
from typing import Callable
from aiogram import Bot, Dispatcher
from config.config import load_config
from src.bootstrap.app import AppContext
from src.bootstrap.middleware import AppMiddleware
from src.handlers.common import callback_router, text_router
from src.handlers.common.start import start_handler
from src.services.user_service import UserService
from src.ui.screen_engine import ScreenEngine
from src.ui.screen_middleware import InjectUserMiddleware, ScreenMiddlewareManager
from src.ui.screen_registry import ScreenRegistry
from src.ui.screen_router import ScreenRouter
from src.webhook.server import WebhookServer
from src.webhook.setup import setup_webhook


# =========================
# LOGGING
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(filename)s:%(lineno)d [%(levelname)s] %(asctime)s - %(message)s",
)

logger = logging.getLogger("shadow.bot")


# =========================
# SAFE SCREEN REGISTRATION
# =========================
def _fallback_register_screens(registry: ScreenRegistry) -> None:
    return


try:
    from src.ui.bootstrap_screens import register_screens as _register_screens
except ImportError:
    _register_screens = _fallback_register_screens  # type: ignore[assignment]


register_screens: Callable[[ScreenRegistry], None] = _register_screens


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
    app.services["user_service"] = UserService()

    # =========================
    # SCREEN SYSTEM
    # =========================
    registry = ScreenRegistry()
    register_screens(registry)

    middleware = ScreenMiddlewareManager()
    middleware.add(InjectUserMiddleware())

    engine = ScreenEngine(registry, middleware)
    router = ScreenRouter(engine)

    # =========================
    # ATTACH TO APP
    # =========================
    app.ui["registry"] = registry
    app.ui["engine"] = engine
    app.ui["router"] = router

    # =========================
    # MIDDLEWARE
    # =========================
    dp.update.outer_middleware(AppMiddleware(app))

    # =========================
    # ROUTERS
    # =========================
    dp.include_router(callback_router.router)
    dp.include_router(text_router.router)

    # =========================
    # HANDLERS
    # =========================
    dp.message.register(start_handler)

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


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Shutdown signal received")