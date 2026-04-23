# src/webhook/server.py

import logging
import asyncio

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import Update

logger = logging.getLogger("shadow.webhook")


class WebhookServer:
    def __init__(self, bot: Bot, dp: Dispatcher, webhook_path: str, secret: str):
        self.bot = bot
        self.dp = dp
        self.webhook_path = webhook_path
        self.secret = secret

    # =========================
    # HANDLE INCOMING UPDATES
    # =========================
    async def handle_webhook(self, request: web.Request):
        try:
            data = await request.json()

            logger.info("Incoming update: %s", data.get("update_id"))

            update = Update(**data)

            await self.dp.feed_update(self.bot, update)

            return web.Response(text="OK")

        except Exception:
            logger.exception("Webhook processing error")
            return web.Response(status=500, text="error")

    # =========================
    # ROUTES
    # =========================
    def setup_routes(self, app: web.Application):
        app.router.add_post(self.webhook_path, self.handle_webhook)

    # =========================
    # SERVER START
    # =========================
    async def run(self, host: str = "0.0.0.0", port: int = 8080):
        app = web.Application()
        self.setup_routes(app)

        runner = web.AppRunner(app)
        await runner.setup()

        site = web.TCPSite(runner, host, port)

        logger.info("Webhook server running on %s:%s", host, port)

        await site.start()

        try:
            while True:
                await asyncio.sleep(3600)
        except asyncio.CancelledError:
            pass
        finally:
            await runner.cleanup()