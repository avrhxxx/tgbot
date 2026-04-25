# =========================================
# GROUP: telegram.routing.core
# FILE: engine.py
# DESCRIPTION:
# Routing engine uses guard (which uses policy.py)
# =========================================

import logging
from typing import Optional, Any

from aiogram_dialog import DialogManager, StartMode

from src.telegram.routing.core.registry import get_route
from src.telegram.routing.core.guard import guard
from src.telegram.permissions.context import UserContext

from src.telegram.states.home import HomeSG, EventsSG, SettingsSG, HelpSG

logger = logging.getLogger(__name__)


STATE_MAP = {
    "home": HomeSG.main,
    "events": EventsSG.main,
    "settings": SettingsSG.main,
    "help": HelpSG.main,
}


class RoutingEngine:

    async def execute(
        self,
        route_id: str,
        dialog_manager: DialogManager,
        user: UserContext,
        **kwargs: Any
    ) -> bool:

        logger.info(
            "Routing request | user=%s role=%s route=%s",
            user.user_id,
            user.role,
            route_id,
        )

        # 🔐 POLICY-BASED GUARD
        if not guard.can_access(user, route_id):
            logger.warning(
                "Access denied | user=%s role=%s route=%s",
                user.user_id,
                user.role,
                route_id,
            )
            return False

        route = get_route(route_id)

        if not route:
            logger.warning("Route not found | %s", route_id)
            return False

        try:
            if route.handler:
                await route.handler(dialog_manager, **kwargs)
                return True

            state = STATE_MAP.get(route.target)

            if not state:
                logger.error("No state mapping for %s", route.target)
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