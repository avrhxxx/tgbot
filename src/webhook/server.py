# src/webhook/server.py
# =========================================
# GROUP: webhook
# FILE: server.py
# DESCRIPTION:
# Lightweight aiohttp webhook server for Telegram updates.
# =========================================

import asyncio
import logging

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

        logger.info("WebhookServer initialized (path=%s)", webhook_path)

    async def handle_webhook(self, request: web.Request):
        try:
            data = await request.json()

            update_id = data.get("update_id")
            logger.info("Incoming update received (id=%s)", update_id)

            update = Update(**data)

            # 🔥 CORE DISPATCH FLOW
            await self.dp.feed_update(self.bot, update)

            logger.info("Update processed successfully (id=%s)", update_id)

            return web.Response(text="OK")

        except Exception:
            logger.exception("Webhook processing error")
            return web.Response(status=500, text="error")

    def setup_routes(self, app: web.Application):
        logger.info("Registering webhook route: %s", self.webhook_path)
        app.router.add_post(self.webhook_path, self.handle_webhook)

    async def run(self, host: str = "0.0.0.0", port: int = 8080):
        logger.info("Starting aiohttp server on %s:%s", host, port)

        app = web.Application()
        self.setup_routes(app)

        runner = web.AppRunner(app)
        await runner.setup()

        site = web.TCPSite(runner, host, port)

        logger.info("Webhook server ready (listening)")

        await site.start()

        try:
            while True:
                await asyncio.sleep(3600)
        finally:
            logger.warning("Shutting down webhook server...")
            await runner.cleanup()