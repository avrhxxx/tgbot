# GROUP: bootstrap
# DESCRIPTION: Telegram entrypoint (Stage 1 - clean runtime launcher)

import asyncio
import signal

from aiogram import Bot, Dispatcher

from src.adapters.telegram.webhook_server import TelegramWebhookServer
from src.config.config import load_config
from src.shared.logging import get_logger

logger = get_logger("bootstrap")


# =========================
# GRACEFUL SHUTDOWN HANDLER
# =========================

shutdown_event = asyncio.Event()


def _handle_shutdown(*_):
    logger.info("🛑 Shutdown signal received")
    shutdown_event.set()


async def main():
    logger.info("🧠 Tiles Survive SYSTEM START (Stage 1)")

    # =========================
    # CONFIG LOAD (FAIL-FAST)
    # =========================
    config = load_config()
    telegram_cfg = config.telegram

    if not telegram_cfg.token:
        raise RuntimeError("Missing TELEGRAM_TOKEN")

    if not telegram_cfg.webhook_secret:
        raise RuntimeError("Missing WEBHOOK_SECRET")

    if not telegram_cfg.webhook_url:
        raise RuntimeError("Missing WEBHOOK_URL")

    # =========================
    # BOT INIT (TRANSPORT ONLY)
    # =========================
    bot = Bot(token=telegram_cfg.token)
    dp = Dispatcher()

    # =========================
    # WEBHOOK SERVER
    # =========================
    server = TelegramWebhookServer(
        bot=bot,
        dp=dp,
        secret=telegram_cfg.webhook_secret
    )

    logger.info("🔌 Telegram adapter initialized")

    # =========================
    # SIGNAL HANDLERS
    # =========================
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, _handle_shutdown)
    loop.add_signal_handler(signal.SIGTERM, _handle_shutdown)

    # =========================
    # RUN SERVER
    # =========================
    server_task = asyncio.create_task(server.run())

    await shutdown_event.wait()

    logger.info("🧹 Shutting down server...")
    server_task.cancel()

    try:
        await server_task
    except asyncio.CancelledError:
        pass

    logger.info("✅ Shutdown complete")


if __name__ == "__main__":
    asyncio.run(main())