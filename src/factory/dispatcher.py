# src/factory/dispatcher.py
# =========================================
# GROUP: factory
# FILE: dispatcher.py
# DESCRIPTION:
# Creates Aiogram Dispatcher instance with dialog support.
# Production-ready minimal setup (no business logic).
# =========================================

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs


def create_dispatcher() -> Dispatcher:
    """
    Creates configured Dispatcher instance.
    """

    # In production we can later swap to RedisStorage
    storage = MemoryStorage()

    dp = Dispatcher(storage=storage)

    # aiogram-dialog integration
    setup_dialogs(dp)

    return dp