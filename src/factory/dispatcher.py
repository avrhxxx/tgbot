# src/factory/dispatcher.py
# =========================================
# GROUP: factory
# FILE: dispatcher.py
# DESCRIPTION:
# Creates Aiogram Dispatcher instance with dialog + routers.
# Production-ready minimal setup.
# =========================================

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from src.telegram.handlers.start import router as start_router
from src.telegram.dialogs.home.window import home_window
from aiogram_dialog import Dialog


def create_dispatcher() -> Dispatcher:
    """
    Creates configured Dispatcher instance.
    """

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # =========================
    # ROUTERS (INPUT LAYER)
    # =========================
    dp.include_router(start_router)

    # =========================
    # DIALOGS (UI LAYER)
    # =========================
    dialog = Dialog(home_window)
    dp.include_router(dialog)

    # aiogram-dialog setup
    setup_dialogs(dp)

    return dp