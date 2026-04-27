# =========================================
# FILE: src/factory/dispatcher.py
# =========================================

import logging
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.handlers.start import router as start_router
from src.handlers.flows.group_message import router as group_router
from src.handlers.n8n_router import router as fallback_router
from src.middlewares.config import ConfigMiddleware

logger = logging.getLogger(__name__)


def create_dispatcher(config) -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())

    dp.update.middleware(ConfigMiddleware(config))

    dp.include_router(start_router)
    dp.include_router(group_router)
    dp.include_router(fallback_router)

    logger.info("Dispatcher ready (UI test mode)")
    return dp