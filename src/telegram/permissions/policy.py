# =========================================
# GROUP: telegram.permissions
# FILE: policy.py
# DESCRIPTION:
# SINGLE SOURCE OF TRUTH for access control.
# Used by routing, guard layer and UI rendering.
# =========================================

import logging
from src.telegram.permissions.roles import Role

logger = logging.getLogger(__name__)


class Permission:
    """
    Represents access rule for actions/routes.
    """

    def __init__(self, allowed_roles: set[Role]):
        self.allowed_roles = allowed_roles

    def allows(self, role: Role) -> bool:
        # OWNER always bypasses all rules
        if role == Role.OWNER:
            return True

        return role in self.allowed_roles


# =========================================================
# ROLE ACCESS LEVELS
# =========================================================

ACCESS_PUBLIC = Permission({
    Role.R3,
    Role.R4,
    Role.R5,
    Role.OWNER,
})

ACCESS_MEMBER = Permission({
    Role.R3,
    Role.R4,
    Role.R5,
    Role.OWNER,
})

ACCESS_OFFICER = Permission({
    Role.R4,
    Role.R5,
    Role.OWNER,
})

ACCESS_LEADER = Permission({
    Role.R5,
    Role.OWNER,
})

ACCESS_OWNER = Permission({
    Role.OWNER,
})


# =========================================================
# ROUTE PERMISSION MAP
# =========================================================

ROUTE_PERMISSIONS: dict[str, Permission] = {
    "home": ACCESS_PUBLIC,
    "events": ACCESS_PUBLIC,
    "quick_join": ACCESS_MEMBER,
    "settings": ACCESS_OFFICER,
    "help": ACCESS_PUBLIC,
    "admin": ACCESS_OWNER,
}


def get_permission(route_id: str) -> Permission:
    """
    Returns permission rule for given route.
    Defaults to PUBLIC access.
    """

    perm = ROUTE_PERMISSIONS.get(route_id, ACCESS_PUBLIC)

    logger.debug(
        "Permission resolved | route=%s roles=%s",
        route_id,
        [r.value for r in perm.allowed_roles],
    )

    return perm