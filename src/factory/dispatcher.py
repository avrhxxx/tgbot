# =========================================
# GROUP: factory
# FILE: dispatcher.py
# DESCRIPTION:
# Aiogram dispatcher factory + UI state injection + router binding
# CLEAN ARCH VERSION (Event Bus UI system)
# =========================================

import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.telegram.routing.core.registry import register_all_routes

from src.ui.controller.ui_controller import UIController
from src.ui.state.ui_state import UIState

logger = logging.getLogger(__name__)


def setup_dispatcher() -> Dispatcher:
    """
    Creates dispatcher with:
    - FSM storage
    - UI state injection middleware
    - route registry bootstrap
    """

    logger.info("Initializing Dispatcher...")

    dp = Dispatcher(storage=MemoryStorage())

    # =========================
    # UI CONTROLLER (EVENT BUS CORE STATE)
    # =========================
    ui_controller = UIController()

    # inject UI state into middleware_data
    @dp.update.middleware()
    async def ui_state_middleware(handler, event, data):
        data["ui_state"] = ui_controller.state
        return await handler(event, data)

    # =========================
    # ROUTES REGISTRATION
    # =========================
    logger.info("Registering routes...")
    register_all_routes()

    logger.info("Dispatcher ready (CLEAN UI MODE)")
    return dp