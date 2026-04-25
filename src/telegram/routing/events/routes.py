# =========================================
# GROUP: telegram.routing.events
# FILE: routes.py
# =========================================

from src.telegram.routing.core.actions import RouteAction
from src.telegram.routing.core.registry import register

EVENTS_HOME = RouteAction(id="events_home", target="events")

EVENTS_ROUTES = [EVENTS_HOME]

for r in EVENTS_ROUTES:
    register(r)