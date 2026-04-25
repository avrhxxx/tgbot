# =========================================
# GROUP: telegram.routing
# FILE: routes.py
# DESCRIPTION:
# SINGLE SOURCE OF TRUTH for all routing actions.
# Central registry (OPTION A architecture).
# =========================================

import logging

from src.telegram.routing.core.actions import RouteAction
from src.telegram.routing.core.registry import register

logger = logging.getLogger(__name__)


# =========================================================
# HOME FLOW
# =========================================================

HOME = RouteAction(id="home", target="home")

EVENTS = RouteAction(id="events", target="events")
SETTINGS = RouteAction(id="settings", target="settings")
HELP = RouteAction(id="help", target="help")

QUICK_JOIN = RouteAction(
    id="quick_join",
    target="events",
)


# =========================================================
# REGISTRATION
# =========================================================

register(HOME)
register(EVENTS)
register(SETTINGS)
register(HELP)
register(QUICK_JOIN)


# =========================================================
# LOGGING
# =========================================================

logger.info(
    "Routing registry initialized | routes=%s",
    ["home", "events", "settings", "help", "quick_join"],
)