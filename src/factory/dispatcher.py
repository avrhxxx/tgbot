# src/factory/dispatcher.py
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
from aiogram_dialog import setup_dialogs, Dialog

from src.telegram.handlers.start import router as start_router
from src.telegram.dialogs.home.window import home_window


logger = logging.getLogger(__name__)


def create_dispatcher() -> Dispatcher:
    """
    Creates configured Dispatcher instance.
    """

    logger.info("Initializing Dispatcher...")

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # =========================
    # ROUTERS (INPUT LAYER)
    # =========================
    logger.info("Registering routers...")
    dp.include_router(start_router)

    # =========================
    # DIALOGS (UI LAYER)
    # =========================
    logger.info("Registering dialogs...")
    dialog = Dialog(home_window)
    dp.include_router(dialog)

    setup_dialogs(dp)

    logger.info("Dispatcher ready")

    return dp