# =========================================
# FILE: src/factory/dispatcher.py
# DESCRIPTION:
# Dispatcher bootstrap (clean shell)
# =========================================

import logging
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.handlers.start import router as start_router
from src.handlers.n8n_bridge import router as flow_router
from src.middlewares.config import ConfigMiddleware

logger = logging.getLogger(__name__)


def create_dispatcher(config) -> Dispatcher:
    logger.info("Starting Dispatcher")

    dp = Dispatcher(storage=MemoryStorage())

    dp.update.middleware(ConfigMiddleware(config))

    dp.include_router(start_router)
    dp.include_router(flow_router)

    logger.info("Dispatcher ready (n8n core mode)")
    return dp