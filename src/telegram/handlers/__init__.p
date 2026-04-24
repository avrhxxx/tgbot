# src/telegram/handlers/__init__.py
# =========================================
# GROUP: telegram.handlers
# FILE: __init__.py
# DESCRIPTION:
# Central router registry for all bot handlers and dialogs.
# =========================================

from aiogram import Dispatcher

from src.telegram.handlers import start
from src.telegram.handlers import home
from src.telegram.handlers import events


def setup_routers(dp: Dispatcher) -> None:
    """
    Registers all routers + dialog systems.
    This is the ONLY entry point for handler wiring.
    """

    # =========================
    # BASIC HANDLERS
    # =========================
    dp.include_router(start.router)

    # =========================
    # FEATURE MODULES
    # =========================
    dp.include_router(home.router)
    dp.include_router(events.router)

    # =========================
    # DIALOG SYSTEM (aiogram-dialog)
    # =========================
    # setup_dialogs(dp) is called in factory/dispatcher.py
    # so we only ensure routers are included here