# =========================================
# GROUP: telegram.routing.core
# FILE: guard.py
# DESCRIPTION:
# Thin access layer using policy.py
# =========================================

import logging

from src.telegram.permissions.policy import get_permission
from src.telegram.permissions.context import UserContext

logger = logging.getLogger(__name__)


class Guard:

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


guard = Guard()