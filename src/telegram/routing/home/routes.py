# =========================================
# GROUP: telegram.routing.home
# FILE: routes.py
# DESCRIPTION:
# Home module routing definitions (feature-based routing v2).
# =========================================

import logging

from src.telegram.routing.core.actions import RouteAction
from src.telegram.routing.core.registry import register

logger = logging.getLogger(__name__)


HOME = RouteAction(id="home", target="home")
EVENTS = RouteAction(id="events", target="events")
SETTINGS = RouteAction(id="settings", target="settings")
HELP = RouteAction(id="help", target="help")

# 🔥 QUICK JOIN (NEW)
QUICK_JOIN = RouteAction(
    id="quick_join",
    target="events",  # tymczasowo kieruje do events (możemy potem podpiąć handler)
)


# auto-registration on import
register(HOME)
register(EVENTS)
register(SETTINGS)
register(HELP)
register(QUICK_JOIN)

logger.info(
    "Home routes registered (%s)",
    ["home", "events", "settings", "help", "quick_join"],
)