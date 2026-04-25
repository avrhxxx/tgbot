# =========================================
# GROUP: telegram.permissions
# FILE: roles.py
# DESCRIPTION:
# Core alliance role system + system admin layer.
# =========================================

import logging
from enum import Enum

logger = logging.getLogger(__name__)


class Role(str, Enum):
    """
    Alliance roles (game layer).
    """

    R3 = "R3"  # Member of alliance
    R4 = "R4"  # Officer of alliance
    R5 = "R5"  # Leader of alliance

    OWNER = "OWNER"  # Bot system owner (out-of-game control layer)

    # -------------------------
    # ROLE LOGIC HELPERS
    # -------------------------

    def is_member(self) -> bool:
        return self in (Role.R3, Role.R4, Role.R5)

    def is_officer(self) -> bool:
        return self in (Role.R4, Role.R5)

    def is_leader(self) -> bool:
        return self == Role.R5

    def is_owner(self) -> bool:
        return self == Role.OWNER

    def is_admin(self) -> bool:
        return self == Role.OWNER