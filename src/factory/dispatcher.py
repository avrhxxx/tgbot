# =========================================
# GROUP: factory
# FILE: dispatcher.py
# DESCRIPTION:
# Minimal clean dispatcher for moderator panel (MVP).
# =========================================

import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.handlers.start import router as start_router
from src.handlers.broadcast import router as broadcast_router

logger = logging.getLogger(__name__)


def create_dispatcher() -> Dispatcher:
    logger.info("Starting Dispatcher (MVP MODE)")

    dp = Dispatcher(storage=MemoryStorage())

    # =========================
    # ROUTERS
    # =========================
    dp.include_router(start_router)
    dp.include_router(broadcast_router)

    logger.info("Dispatcher ready")
    return dp