# =========================================
# FILE: src/factory/dispatcher.py
# DESCRIPTION:
# Clean dispatcher with feature routers
# =========================================

import logging
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.handlers.start import router as start_router
from src.handlers.flows.group_message import router as group_message_router
from src.middlewares.config import ConfigMiddleware

logger = logging.getLogger(__name__)


def create_dispatcher(config) -> Dispatcher:
    logger.info("Starting Dispatcher")

    dp = Dispatcher(storage=MemoryStorage())

    # middleware
    dp.update.middleware(ConfigMiddleware(config))

    # routers (FEATURE-BASED)
    dp.include_router(start_router)
    dp.include_router(group_message_router)

    logger.info("Dispatcher ready (clean flow architecture)")
    return dp