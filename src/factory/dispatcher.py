# =========================================
# GROUP: factory
# FILE: dispatcher.py
# DESCRIPTION:
# Creates Aiogram Dispatcher instance with routers + dialogs.
# OPTION A routing architecture (central registry).
# =========================================

import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

# =========================
# ROUTERS
# =========================
from src.telegram.handlers.start import router as start_router

# =========================
# DIALOGS
# =========================
from src.telegram.dialogs.home.home_dialog import home_dialog
from src.telegram.dialogs.home.events_dialog import events_dialog
from src.telegram.dialogs.home.settings_dialog import settings_dialog
from src.telegram.dialogs.home.help_dialog import help_dialog
from src.telegram.dialogs.register.register_dialog import register_dialog  # 🔥 REQUIRED

# =========================
# ROUTING (SIDE EFFECT IMPORTS)
# =========================
import src.telegram.routing.routes  # noqa

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
    # DIALOGS
    # =========================
    logger.info("Registering dialogs...")

    dialogs = [
        register_dialog,  # onboarding MUST BE FIRST
        home_dialog,
        events_dialog,
        settings_dialog,
        help_dialog,
    ]

    for dialog in dialogs:
        dp.include_router(dialog)

    setup_dialogs(dp)

    logger.info("Dispatcher ready (OPTION A enabled)")

    return dp