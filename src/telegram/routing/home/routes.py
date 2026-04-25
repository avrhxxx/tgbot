# =========================================
# GROUP: telegram.routing.home
# FILE: routes.py
# DESCRIPTION:
# Home route definitions
# =========================================

from src.telegram.routing.core.actions import RouteAction
from src.telegram.routing.core.registry import register

HOME = RouteAction(id="home", target="home")
EVENTS = RouteAction(id="events", target="events")
SETTINGS = RouteAction(id="settings", target="settings")
HELP = RouteAction(id="help", target="help")
QUICK_JOIN = RouteAction(id="quick_join", target="events")


HOME_ROUTES = [HOME, EVENTS, SETTINGS, HELP, QUICK_JOIN]

for r in HOME_ROUTES:
    register(r)