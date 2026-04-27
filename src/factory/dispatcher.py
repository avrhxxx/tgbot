from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.handlers.start import router as start_router
from src.dialogs import register_dialogs

from src.middlewares.config import ConfigMiddleware  # 👈 ADD

import logging

logger = logging.getLogger(__name__)


def create_dispatcher(config) -> Dispatcher:
    logger.info("Starting Dispatcher")

    dp = Dispatcher(storage=MemoryStorage())

    # =========================
    # MIDDLEWARES
    # =========================
    dp.update.middleware(ConfigMiddleware(config))  # 👈 FIX

    # ROUTERS
    dp.include_router(start_router)

    # DIALOGS
    register_dialogs(dp)

    logger.info("Dispatcher ready")
    return dp