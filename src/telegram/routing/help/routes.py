# =========================================
# GROUP: telegram.routing.help
# FILE: routes.py
# DESCRIPTION:
# Help module routing definitions.
# =========================================

import logging

from src.telegram.routing.core.actions import RouteAction
from src.telegram.routing.core.registry import register

logger = logging.getLogger(__name__)


HELP_HOME = RouteAction(id="help_home", target="help")

register(HELP_HOME)

logger.info("Help routes registered")