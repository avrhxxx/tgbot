# =========================================
# GROUP: factory
# FILE: dispatcher.py
# DESCRIPTION:
# Creates Aiogram Dispatcher instance with dialog + routers.
# Production-ready minimal setup.
# =========================================

import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from src.telegram.handlers.start import router as start_router
from src.telegram.dialogs.home.dialog import home_dialog


logger = logging.getLogger(__name__)


def create_dispatcher() -> Dispatcher:
    logger.info("Initializing Dispatcher...")

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # =========================
    # ROUTERS
    # =========================
    logger.info("Registering routers...")
    dp.include_router(start_router)

    # =========================
    # DIALOGS (CORRECT WAY)
    # =========================
    logger.info("Registering dialogs...")
    dp.include_router(home_dialog)

    setup_dialogs(dp)

    logger.info("Dispatcher ready")

    return dp