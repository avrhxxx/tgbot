# =========================================
# GROUP: telegram.routing.core
# FILE: binder.py
# DESCRIPTION:
# UI → Routing v2 binding layer.
# =========================================

import logging
from typing import Callable, Any

from aiogram_dialog import DialogManager

from src.telegram.routing.core.engine import engine

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
        logger.info("UI click intercepted | route_id=%s", route_id)

        success = await engine.execute(
            route_id=route_id,
            dialog_manager=dialog_manager,
        )

        if not success:
            logger.warning("Route execution failed | route_id=%s", route_id)

    return handler