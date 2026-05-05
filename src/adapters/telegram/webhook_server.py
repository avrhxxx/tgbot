# src/adapters/telegram/webhook_server.py
# GROUP: adapters.telegram
# DESCRIPTION: Production-ready Telegram webhook entrypoint (Railway-safe)

import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import Update

from src.adapters.telegram.handler import handle_telegram_text
from src.shared.logging import get_logger

logger = get_logger("TelegramWebhook")


class TelegramWebhookServer:
    """
    Thin transport layer:
    Telegram Update → extract text → send to adapter → return OK
    """

    def __init__(self, bot: Bot, dp: Dispatcher, secret: str):
        self.bot = bot
        self.dp = dp
        self.secret = secret

    async def handle_update(self, request: web.Request):
        try:
            data = await request.json()
            update = Update(**data)

            message = update.message
            if not message or not message.text:
                logger.info("Ignored update (no text message)")
                return web.Response(text="ignored")

            text = message.text

            logger.info(f"Incoming Telegram message: {text}")

            result = await handle_telegram_text(text)

            logger.info(f"Response generated: {result}")

            return web.Response(text="ok")

        except Exception as e:
            logger.exception(f"Webhook error: {e}")
            return web.Response(status=500)

    def setup(self, app: web.Application):
        app.router.add_post("/webhook", self.handle_update)

    async def run(self, host: str = "0.0.0.0", port: int = 8080):
        app = web.Application()
        self.setup(app)

        runner = web.AppRunner(app)
        await runner.setup()

        site = web.TCPSite(runner, host, port)
        await site.start()

        logger.info("Telegram webhook server running")

        while True:
            await asyncio.sleep(3600)