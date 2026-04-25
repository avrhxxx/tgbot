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

# =========================
# ROUTERS
# =========================
from src.telegram.handlers.start import router as start_router

# =========================
# DIALOGS (CRITICAL)
# =========================
from src.telegram.dialogs.home.home_dialog import home_dialog
from src.telegram.dialogs.home.events_dialog import events_dialog
from src.telegram.dialogs.home.settings_dialog import settings_dialog
from src.telegram.dialogs.home.help_dialog import help_dialog

# ⚠️ REGISTER / ONBOARDING DIALOG (MISSING FIX)
# jeśli go nie masz → bot będzie crashował na RegisterSG
from src.telegram.dialogs.register.register_dialog import register_dialog  # noqa

# =========================
# ROUTING (side effects)
# =========================
import src.telegram.routing.home.routes  # noqa
import src.telegram.routing.events.routes  # noqa
import src.telegram.routing.help.routes  # noqa
import src.telegram.routing.settings.routes  # noqa

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

    dp.include_router(home_dialog)
    dp.include_router(events_dialog)
    dp.include_router(settings_dialog)
    dp.include_router(help_dialog)

    # 🔥 CRITICAL FIX: register onboarding dialog
    dp.include_router(register_dialog)

    setup_dialogs(dp)

    logger.info("Dispatcher ready")

    return dp