# src/bootstrap/bot.py
# GROUP: bootstrap
# DESCRIPTION: Application entrypoint for Shadow AI Wiki Bot

import asyncio
import logging
import aiohttp

from aiogram import Bot, Dispatcher

from src.config.config import load_config
from src.handlers.telegram_handler import handle_message
from src.webhook.server import WebhookServer
from src.webhook.setup import setup_webhook


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bootstrap")


# =========================
# 🔥 DEBUG GEMINI MODELS
# =========================
async def debug_list_models(api_key: str):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()

                logger.info("====================================")
                logger.info("🔍 GEMINI AVAILABLE MODELS:")
                logger.info(data)
                logger.info("====================================")

    except Exception as e:
        logger.exception("Failed to fetch Gemini models: %s", e)


async def main():
    config = load_config()

    # =========================
    # 🔥 DEBUG CALL (TEMP)
    # =========================
    await debug_list_models(config.gemini.api_key)

    # =========================
    # BOT + DISPATCHER
    # =========================
    bot = Bot(token=config.telegram.token)
    dp = Dispatcher()

    # 🔥 REGISTER HANDLER (CRITICAL FIX)
    dp.message.register(handle_message)

    # =========================
    # WEBHOOK SERVER
    # =========================
    webhook = WebhookServer(
        bot=bot,
        dp=dp,
        webhook_path="/webhook",
        secret=config.telegram.webhook_secret
    )

    # =========================
    # SET WEBHOOK (Railway-ready)
    # =========================
    await setup_webhook(
        bot=bot,
        webhook_url=config.telegram.webhook_url,
        secret=config.telegram.webhook_secret
    )

    # =========================
    # RUN SERVER
    # =========================
    logger.info("Starting Shadow AI Wiki Bot...")
    await webhook.run()


if __name__ == "__main__":
    asyncio.run(main())