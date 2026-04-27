# =========================================
# FILE: src/factory/dispatcher.py
# DESCRIPTION:
# Dispatcher factory (clean n8n-style version)
# =========================================

import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.handlers.start import router as start_router
from src.handlers.messages import router as message_router
from src.handlers.announcement_callbacks import router as callback_router

from src.middlewares.config import ConfigMiddleware

logger = logging.getLogger(__name__)


def create_dispatcher(config) -> Dispatcher:
    logger.info("Starting Dispatcher")

    dp = Dispatcher(storage=MemoryStorage())

    # =========================
    # MIDDLEWARES
    # =========================
    dp.update.middleware(ConfigMiddleware(config))

    # =========================
    # ROUTERS
    # =========================
    dp.include_router(start_router)
    dp.include_router(message_router)
    dp.include_router(callback_router)

    logger.info("Dispatcher ready (n8n-style flow enabled)")
    return dp