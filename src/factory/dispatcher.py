# =========================================
# FILE: src/factory/dispatcher.py
# =========================================

import logging
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram_dialog import setup_dialogs

from src.handlers.start import router as start_router
from src.middlewares.config import ConfigMiddleware

logger = logging.getLogger(__name__)


def create_dispatcher(config) -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())

    # middleware
    dp.update.middleware(ConfigMiddleware(config))

    # routers
    dp.include_router(start_router)

    # 🔥 CRITICAL
    setup_dialogs(dp)

    logger.info("Dispatcher ready (dialogs mode)")
    return dp