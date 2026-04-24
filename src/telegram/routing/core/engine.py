# =========================================
# GROUP: telegram.routing.core
# FILE: engine.py
# =========================================

import logging
from typing import Optional, Any

from aiogram_dialog import DialogManager, StartMode

from src.telegram.routing.core.registry import get_route
from src.telegram.routing.core.actions import RouteAction

from src.telegram.states.home import HomeSG, EventsSG, SettingsSG, HelpSG

logger = logging.getLogger(__name__)


STATE_MAP = {
    "home": HomeSG.main,
    "events": EventsSG.main,
    "settings": SettingsSG.main,
    "help": HelpSG.main,
}


class RoutingEngine:

    def __init__(self):
        logger.info("RoutingEngine initialized")

    async def execute(
        self,
        route_id: str,
        dialog_manager: DialogManager,
        **kwargs: Any
    ) -> bool:

        logger.info("Routing request | route_id=%s", route_id)

        route: Optional[RouteAction] = get_route(route_id)

        if not route:
            logger.warning("Route not found | %s", route_id)
            return False

        try:
            if route.handler:
                await route.handler(dialog_manager, **kwargs)
                return True

            state = STATE_MAP.get(route.target)

            if not state:
                logger.error("No state mapping for target=%s", route.target)
                return False

            logger.info("Starting dialog | %s", route.target)

            await dialog_manager.start(
                state=state,
                mode=StartMode.NORMAL,
            )

            return True

        except Exception as e:
            logger.exception("Routing error | %s", str(e))
            return False


engine = RoutingEngine()