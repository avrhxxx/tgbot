# =========================================
# GROUP: telegram.routing.core
# FILE: registry.py
# DESCRIPTION:
# Central routing registry for routing v2 system.
# Stores and resolves RouteAction objects.
# =========================================

import logging
from typing import Dict, Optional

from src.telegram.routing.core.actions import RouteAction

logger = logging.getLogger(__name__)

ROUTES: Dict[str, RouteAction] = {}


def register(action: RouteAction) -> None:
    """
    Registers a routing action globally.
    """
    ROUTES[action.id] = action
    logger.debug("Route registered: %s -> %s", action.id, action.target)


def get_route(route_id: str) -> Optional[RouteAction]:
    """
    Retrieves route by id.
    """
    route = ROUTES.get(route_id)

    if not route:
        logger.warning("Route not found: %s", route_id)

    return route