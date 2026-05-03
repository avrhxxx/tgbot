# src/webhook/server.py
# GROUP: webhook
# DESCRIPTION: Minimal webhook server (CLEAN BOOT MODE)

import asyncio
import logging

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import Update


logger = logging.getLogger("webhook.server")


class WebhookServer:
    def __init__(self, bot: Bot, dp: Dispatcher, webhook_path: str, secret: str):
        self.bot = bot
        self.dp = dp
        self.webhook_path = webhook_path
        self.secret = secret

    async def handle(self, request: web.Request):
        try:
            data = await request.json()
            update = Update(**data)

            await self.dp.feed_update(self.bot, update)

            return web.Response(text="ok")

        except Exception as e:
            logger.exception("Webhook error: %s", e)
            return web.Response(status=500)

    def setup_routes(self, app: web.Application):
        app.router.add_post(self.webhook_path, self.handle)

    async def run(self, host: str = "0.0.0.0", port: int = 8080):
        app = web.Application()
        self.setup_routes(app)

        runner = web.AppRunner(app)
        await runner.setup()

        site = web.TCPSite(runner, host, port)
        await site.start()

        logger.info("Webhook server running on %s:%s", host, port)

        # keep alive
        while True:
            await asyncio.sleep(3600)