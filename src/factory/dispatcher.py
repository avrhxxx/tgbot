# =========================================
# GROUP: factory
# FILE: dispatcher.py
# DESCRIPTION:
# Aiogram dispatcher setup (MVP clean version).
# =========================================

import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.handlers import register_handlers

logger = logging.getLogger(__name__)


def create_dispatcher() -> Dispatcher:
    logger.info("Starting Dispatcher (MVP MODE)")

    dp = Dispatcher(storage=MemoryStorage())

    register_handlers(dp)

    logger.info("Dispatcher ready")
    return dp