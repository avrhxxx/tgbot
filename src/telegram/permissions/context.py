# =========================================
# GROUP: telegram.permissions
# FILE: context.py
# DESCRIPTION:
# Runtime user identity context used by routing, guard and engine layers.
# =========================================

import logging
from dataclasses import dataclass

from src.telegram.permissions.roles import Role

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class UserContext:
    """
    Immutable runtime user context.
    This object is passed through routing engine and permission guard.
    """

    user_id: int
    role: Role

    # -------------------------
    # ROLE HELPERS (CONVENIENCE)
    # -------------------------

    def is_owner(self) -> bool:
        return self.role == Role.OWNER

    def is_member(self) -> bool:
        return self.role in (Role.R3, Role.R4, Role.R5)

    def is_officer(self) -> bool:
        return self.role in (Role.R4, Role.R5)

    def is_leader(self) -> bool:
        return self.role == Role.R5

    def is_admin(self) -> bool:
        return self.role == Role.OWNER