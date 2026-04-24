# =========================================
# GROUP: telegram.routing.core
# FILE: engine.py
# DESCRIPTION:
# Routing execution engine (v2 bridge layer).
#
# Bridges UI layer (aiogram-dialog buttons)
# with routing v2 system (RouteAction registry).
#
# Responsibilities:
# - Resolve route_id from UI actions
# - Fetch RouteAction from registry
# - Execute navigation logic
# - Provide safe logging & fallback handling
# =========================================

import logging
from typing import Optional, Any

from aiogram_dialog import DialogManager

from src.telegram.routing.core.registry import get_route
from src.telegram.routing.core.actions import RouteAction

logger = logging.getLogger(__name__)


class RoutingEngine:
    """
    Core execution engine for routing v2 system.

    This is the ONLY layer that UI should talk to.
    """

    def __init__(self):
        logger.info("RoutingEngine initialized")

    async def execute(
        self,
        route_id: str,
        dialog_manager: DialogManager,
        **kwargs: Any
    ) -> bool:
        """
        Executes navigation based on route_id.

        Returns:
            bool: True if route was successfully executed
        """

        logger.info("Routing request received | route_id=%s", route_id)

        route: Optional[RouteAction] = get_route(route_id)

        if not route:
            logger.warning("Route not found | route_id=%s", route_id)
            return False

        logger.info(
            "Route resolved | id=%s target=%s",
            route.id,
            route.target
        )

        # =========================================
        # EXECUTION STRATEGY
        # =========================================

        try:
            # 1. If custom handler exists → execute it
            if route.handler:
                logger.info("Executing custom route handler | id=%s", route.id)
                await route.handler(dialog_manager, **kwargs)
                return True

            # 2. Default behavior → switch dialog state
            logger.info("Switching dialog state | target=%s", route.target)

            await dialog_manager.switch_to(route.target)

            return True

        except Exception as e:
            logger.exception(
                "Routing execution failed | route_id=%s error=%s",
                route_id,
                str(e)
            )
            return False


# Global engine instance (simple singleton pattern)
engine = RoutingEngine()