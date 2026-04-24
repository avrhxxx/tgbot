# =========================================
# GROUP: telegram.routing.events
# FILE: routes.py
# DESCRIPTION:
# Events module routing definitions.
# =========================================

import logging

from src.telegram.routing.core.actions import RouteAction
from src.telegram.routing.core.registry import register

logger = logging.getLogger(__name__)


EVENTS_HOME = RouteAction(id="events_home", target="events")

register(EVENTS_HOME)

logger.info("Events routes registered")