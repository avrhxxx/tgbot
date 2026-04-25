# =========================================
# GROUP: telegram.routing.core
# FILE: registry.py
# DESCRIPTION:
# Central route registry loader (no imports scattered in modules)
# =========================================

import logging

logger = logging.getLogger(__name__)

ROUTES = {}


def register(route):
    ROUTES[route.id] = route
    logger.debug("Route registered: %s", route.id)


def get_route(route_id: str):
    return ROUTES.get(route_id)


def register_all_routes():
    """
    Import all route modules ONCE here.
    Prevents circular imports and missing route issues.
    """

    logger.info("Bootstrapping route modules...")

    # HOME
    from src.telegram.routing.home.routes import HOME_ROUTES  # noqa

    # EVENTS
    from src.telegram.routing.events.routes import EVENTS_ROUTES  # noqa

    # HELP
    from src.telegram.routing.help.routes import HELP_ROUTES  # noqa

    logger.info("All routes registered")