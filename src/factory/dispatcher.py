# src/factory/dispatcher.py
# DESCRIPTION:
# Dispatcher setup with dialog support.

import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.handlers.start import router as start_router
from src.dialogs import register_dialogs

logger = logging.getLogger(__name__)


def create_dispatcher() -> Dispatcher:
    logger.info("Starting Dispatcher")

    dp = Dispatcher(storage=MemoryStorage())

    # ROUTERS
    dp.include_router(start_router)

    # DIALOGS
    register_dialogs(dp)

    logger.info("Dispatcher ready")
    return dp