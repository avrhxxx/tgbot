import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import load_config
from src.handlers import echo

from src.webhook.setup import setup_webhook
from src.webhook.server import WebhookServer


logger = logging.getLogger(__name__)


# =========================
# MAIN
# =========================

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )

    logger.info("Starting bot (WEBHOOK MODE)")

    config = load_config()

    bot = Bot(
        token=config.tg_bot.token,
        parse_mode="HTML",
    )

    dp = Dispatcher()
    dp.include_router(echo.router)

    # =========================
    # SET WEBHOOK
    # =========================
    await setup_webhook(
        bot=bot,
        webhook_url=config.tg_bot.webhook_url,
        secret=config.tg_bot.webhook_secret,
    )

    # =========================
    # START SERVER
    # =========================
    server = WebhookServer(
        bot=bot,
        dp=dp,
        webhook_path="/webhook",
        secret=config.tg_bot.webhook_secret,
    )

    await server.run(port=8080)


# =========================
# ENTRYPOINT
# =========================

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")