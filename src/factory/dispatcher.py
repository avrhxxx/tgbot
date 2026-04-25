# =========================================
# GROUP: factory
# FILE: dispatcher.py
# =========================================

import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from src.telegram.handlers.start import router as start_router

from src.telegram.dialogs.home.home_dialog import home_dialog
from src.telegram.dialogs.home.events_dialog import events_dialog
from src.telegram.dialogs.home.settings_dialog import settings_dialog
from src.telegram.dialogs.home.help_dialog import help_dialog

import src.telegram.routing.home.routes  # noqa

logger = logging.getLogger(__name__)


def create_dispatcher() -> Dispatcher:
    logger.info("Initializing Dispatcher...")

    dp = Dispatcher(storage=MemoryStorage())

    logger.info("Registering routers...")
    dp.include_router(start_router)

    logger.info("Registering dialogs...")

    dp.include_router(home_dialog)
    dp.include_router(events_dialog)
    dp.include_router(settings_dialog)
    dp.include_router(help_dialog)

    setup_dialogs(dp)

    logger.info("Dispatcher ready")

    return dp