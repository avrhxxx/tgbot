# =========================================
# FILE: src/factory/dispatcher.py
# DESCRIPTION:
# Dispatcher factory with routers + dialogs
# =========================================

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.handlers.start import router as start_router
from src.dialogs.panel.dialog import router as panel_router  # 🔥 DODANE
from src.dialogs import register_dialogs

from src.middlewares.config import ConfigMiddleware

import logging

logger = logging.getLogger(__name__)


def create_dispatcher(config) -> Dispatcher:
    logger.info("Starting Dispatcher")

    dp = Dispatcher(storage=MemoryStorage())

    # =========================
    # MIDDLEWARES
    # =========================
    dp.update.middleware(ConfigMiddleware(config))

    # =========================
    # ROUTERS
    # =========================
    dp.include_router(start_router)
    dp.include_router(panel_router)  # 🔥 KLUCZOWE

    # =========================
    # DIALOGS
    # =========================
    register_dialogs(dp)

    logger.info("Dispatcher ready")
    return dp