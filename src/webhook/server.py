import logging
import asyncio

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import Update

logger = logging.getLogger(__name__)


# =========================
# WEBHOOK SERVER CLASS
# =========================
class WebhookServer:
    def __init__(self, bot: Bot, dp: Dispatcher, webhook_path: str, secret: str):
        self.bot = bot
        self.dp = dp
        self.webhook_path = webhook_path
        self.secret = secret

    # =========================
    # HANDLER TELEGRAM UPDATES
    # =========================
    async def handle_webhook(self, request: web.Request):
        try:
            data = await request.json()

            logger.info("Incoming webhook update: %s", data.get("update_id"))

            # =========================
            # FIX: proper aiogram v3 parsing
            # =========================
            update = Update.model_validate(data)

            await self.dp.feed_update(self.bot, update)

            return web.Response(text="OK")

        except Exception as e:
            logger.exception("Webhook error: %s", e)
            return web.Response(status=500, text="Internal Error")

    # =========================
    # SETUP ROUTES
    # =========================
    def setup_routes(self, app: web.Application):
        app.router.add_post(self.webhook_path, self.handle_webhook)

    # =========================
    # START SERVER
    # =========================
    async def run(self, host: str = "0.0.0.0", port: int = 8080):
        app = web.Application()

        self.setup_routes(app)

        runner = web.AppRunner(app)
        await runner.setup()

        site = web.TCPSite(runner, host, port)

        logger.info("Starting webhook server on %s:%s", host, port)

        await site.start()

        # =========================
        # KEEP ALIVE LOOP (RAILWAY SAFE)
        # =========================
        try:
            while True:
                await asyncio.sleep(3600)
        except (asyncio.CancelledError, KeyboardInterrupt):
            logger.info("Shutting down webhook server...")

        await runner.cleanup()