# =========================================
# GROUP: telegram.routing.core
# FILE: guard.py
# DESCRIPTION:
# Central routing guard layer (permissions, future rate limits, audit hooks).
# =========================================

import logging

from src.telegram.permissions.context import UserContext
from src.telegram.permissions.policy import get_permission

logger = logging.getLogger(__name__)


class RoutingGuard:
    """
    Responsible ONLY for access decisions.
    No routing logic here.
    """

    def can_access(self, user: UserContext, route_id: str) -> bool:
        permission = get_permission(route_id)

        allowed = permission.allows(user.role)

        logger.debug(
            "Guard check | user=%s role=%s route=%s allowed=%s",
            user.user_id,
            user.role,
            route_id,
            allowed,
        )

        return allowed


# global instance
guard = RoutingGuard()