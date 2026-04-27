# =========================================
# FILE: src/factory/dispatcher.py
# DESCRIPTION:
# Dispatcher factory (minimal thin shell for n8n routing)
# =========================================

import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.handlers.start import router as start_router
from src.handlers.n8n_router import router as n8n_router
from src.middlewares.config import ConfigMiddleware

logger = logging.getLogger(__name__)


def create_dispatcher(config) -> Dispatcher:
    logger.info("🚀 Starting Dispatcher (MVP n8n mode)")

    dp = Dispatcher(storage=MemoryStorage())

    # Middleware
    dp.update.middleware(ConfigMiddleware(config))

    # Routers
    dp.include_router(start_router)
    dp.include_router(n8n_router)

    logger.info("✅ Dispatcher ready (MVP: 1 flow only)")
    return dp