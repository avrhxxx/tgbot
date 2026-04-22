import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    setup_application
)
from aiohttp import web

from config import Config, load_config
from src.handlers import echo


logger = logging.getLogger(__name__)

WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = "shadow_secret"


async def on_startup(bot: Bot):
    config: Config = load_config()

    webhook_url = f"{config.web.base_url}{WEBHOOK_PATH}"

    await bot.set_webhook(
        url=webhook_url,
        secret_token=WEBHOOK_SECRET,
        drop_pending_updates=True
    )

    logger.info(f"Webhook registered: {webhook_url}")


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
               "[%(asctime)s] - %(name)s - %(message)s",
    )

    logger.info("Starting bot (WEBHOOK MODE)")

    config: Config = load_config()

    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher()

    dp.include_router(echo.router)

    app = web.Application()

    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    ).register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    app.on_startup.append(lambda _: on_startup(bot))

    web.run_app(
        app,
        host="0.0.0.0",
        port=config.web.port
    )


if __name__ == "__main__":
    main()