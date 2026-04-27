# =========================================
# FILE: src/factory/dispatcher.py
# DESCRIPTION:
# Dispatcher factory (thin shell architecture - n8n driven)
# =========================================

import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.handlers.start import router as start_router
from src.handlers.n8n_router import router as n8n_router
from src.middlewares.config import ConfigMiddleware

logger = logging.getLogger(__name__)


def create_dispatcher(config) -> Dispatcher:
    logger.info("🚀 Starting Dispatcher (thin shell mode)")

    dp = Dispatcher(storage=MemoryStorage())

    # =========================
    # MIDDLEWARES
    # =========================
    dp.update.middleware(ConfigMiddleware(config))

    # =========================
    # ROUTERS
    # =========================
    dp.include_router(start_router)
    dp.include_router(n8n_router)

    logger.info("✅ Dispatcher ready (n8n-first architecture)")
    return dp