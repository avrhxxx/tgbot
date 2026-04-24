# =========================================
# GROUP: telegram.permissions
# FILE: policy.py
# DESCRIPTION:
# Permission policy matrix for alliance system.
# Defines what each role can access.
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
# 🔥 GAME ACTION PERMISSIONS (ALLIANCE SYSTEM)
# =========================================================

# Basic access (all members)
ACCESS_PUBLIC = Permission({
    Role.R3,
    Role.R4,
    Role.R5,
    Role.OWNER,
})

# Quick join, basic gameplay actions
ACCESS_MEMBER = Permission({
    Role.R3,
    Role.R4,
    Role.R5,
    Role.OWNER,
})

# Officer-level actions (R4+)
ACCESS_OFFICER = Permission({
    Role.R4,
    Role.R5,
    Role.OWNER,
})

# Leader-level actions (R5+)
ACCESS_LEADER = Permission({
    Role.R5,
    Role.OWNER,
})

# System-only actions (bot owner)
ACCESS_OWNER = Permission({
    Role.OWNER,
})


# =========================================================
# ROUTE PERMISSION MAP (IMPORTANT FOR ROUTING V2)
# =========================================================

ROUTE_PERMISSIONS: dict[str, Permission] = {
    # home is always public
    "home": ACCESS_PUBLIC,

    # gameplay
    "events": ACCESS_PUBLIC,
    "quick_join": ACCESS_MEMBER,

    # management
    "settings": ACCESS_OFFICER,
    "help": ACCESS_PUBLIC,

    # future admin/system routes
    "admin": ACCESS_OWNER,
}


def get_permission(route_id: str) -> Permission:
    """
    Returns permission rule for given route.
    Defaults to public access if not defined.
    """
    perm = ROUTE_PERMISSIONS.get(route_id, ACCESS_PUBLIC)

    logger.debug(
        "Permission resolved | route=%s allowed_roles=%s",
        route_id,
        [r.value for r in perm.allowed_roles],
    )

    return perm