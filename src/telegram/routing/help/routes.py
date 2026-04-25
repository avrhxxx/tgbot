# =========================================
# GROUP: telegram.routing.help
# FILE: routes.py
# =========================================

from src.telegram.routing.core.actions import RouteAction
from src.telegram.routing.core.registry import register

HELP_HOME = RouteAction(id="help_home", target="help")

HELP_ROUTES = [HELP_HOME]

for r in HELP_ROUTES:
    register(r)