# =========================================
# GROUP: factory
# FILE: dispatcher.py
# DESCRIPTION:
# Aiogram dispatcher (clean UI engine injection)
# =========================================

import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.telegram.routing.core.registry import register_all_routes
from src.ui.controller.ui_controller import UIController

logger = logging.getLogger(__name__)


def setup_dispatcher() -> Dispatcher:
    logger.info("Starting Dispatcher (CLEAN UI MODE)")

    dp = Dispatcher(storage=MemoryStorage())

    ui_controller = UIController()

    # FIX: proper middleware signature (aiogram v3 safe)
    @dp.update.middleware()
    async def ui_middleware(handler, event, data):
        data["ui"] = ui_controller
        return await handler(event, data)

    register_all_routes()

    logger.info("Dispatcher ready")
    return dp