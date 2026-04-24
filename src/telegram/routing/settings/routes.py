# =========================================
# GROUP: telegram.routing.settings
# FILE: routes.py
# DESCRIPTION:
# Settings module routing definitions.
# =========================================

import logging

from src.telegram.routing.core.actions import RouteAction
from src.telegram.routing.core.registry import register

logger = logging.getLogger(__name__)


SETTINGS_HOME = RouteAction(id="settings_home", target="settings")

register(SETTINGS_HOME)

logger.info("Settings routes registered")