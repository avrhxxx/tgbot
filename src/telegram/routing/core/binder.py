# =========================================
# GROUP: telegram.routing.core
# FILE: binder.py
# DESCRIPTION:
# UI → Routing v2 binding layer.
# Injects UserContext safely via runtime store.
# =========================================

import logging
from typing import Callable, Any

from aiogram_dialog import DialogManager

from src.telegram.routing.core.engine import engine
from src.services.user.context_store import user_context_store

logger = logging.getLogger(__name__)


def route_click(route_id: str) -> Callable:
    """
    Converts route_id into aiogram-dialog on_click handler.
    """

    async def handler(
        callback: Any,
        button: Any,
        dialog_manager: DialogManager,
    ) -> None:

        user_id = callback.from_user.id if callback.from_user else None

        logger.info("UI click intercepted | route_id=%s user_id=%s", route_id, user_id)

        if not user_id:
            logger.warning("Missing user_id in callback")
            return

        user = user_context_store.get(user_id)

        if not user:
            logger.warning("Missing UserContext | route_id=%s user_id=%s", route_id, user_id)
            return

        success = await engine.execute(
            route_id=route_id,
            dialog_manager=dialog_manager,
            user=user,
        )

        if not success:
            logger.warning("Route execution failed | route_id=%s", route_id)

    return handler