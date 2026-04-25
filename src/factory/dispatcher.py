# =========================================
# GROUP: factory
# FILE: dispatcher.py
# DESCRIPTION:
# Creates Aiogram Dispatcher instance with dialog + routers.
# Production-ready minimal setup.
# =========================================

import logging

from aiogram import Dispatcher, BaseMiddleware
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs, DialogManager

from src.telegram.handlers.start import router as start_router

# =========================
# DIALOGS (HOME MODULE)
# =========================
from src.telegram.dialogs.home.home_dialog import home_dialog
from src.telegram.dialogs.home.events_dialog import events_dialog
from src.telegram.dialogs.home.settings_dialog import settings_dialog
from src.telegram.dialogs.home.help_dialog import help_dialog

# =========================
# DIALOGS (REGISTER MODULE)
# =========================
from src.telegram.dialogs.register.register_dialog import register_dialog

# =========================
# CONTEXT
# =========================
from src.telegram.permissions.context_builder import context_builder

# 🔥 CRITICAL: routing initialization (must be imported for side-effects)
import src.telegram.routing.home.routes  # noqa

logger = logging.getLogger(__name__)


# =========================================
# MIDDLEWARE: USER CONTEXT INJECTION
# =========================================
class UserContextMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):

        dialog_manager: DialogManager | None = data.get("dialog_manager")

        if dialog_manager and getattr(event, "from_user", None):
            context = await context_builder.build(event.from_user)
            dialog_manager.middleware_data["user_context"] = context

        return await handler(event, data)


def create_dispatcher() -> Dispatcher:
    logger.info("Initializing Dispatcher...")

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # =========================
    # MIDDLEWARE
    # =========================
    logger.info("Registering middleware...")
    dp.message.middleware(UserContextMiddleware())
    dp.callback_query.middleware(UserContextMiddleware())

    # =========================
    # ROUTERS
    # =========================
    logger.info("Registering routers...")
    dp.include_router(start_router)

    # =========================
    # DIALOGS
    # =========================
    logger.info("Registering dialogs...")

    # home
    dp.include_router(home_dialog)
    dp.include_router(events_dialog)
    dp.include_router(settings_dialog)
    dp.include_router(help_dialog)

    # register
    dp.include_router(register_dialog)

    setup_dialogs(dp)

    logger.info("Dispatcher ready")

    return dp