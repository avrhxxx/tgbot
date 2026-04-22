from dataclasses import dataclass
from typing import Optional

from src.core.state_store import state_store


@dataclass(frozen=True)
class RoleContext:
    """
    Final resolved role context for UI rendering.
    """
    user_id: int
    real_role: str
    effective_role: str
    is_demo_active: bool


def resolve_role(user_id: int, real_role: str) -> RoleContext:
    """
    SINGLE SOURCE OF TRUTH for role resolution.

    Flow:
    - real_role = role from production system (future Google Sheets)
    - demo_role = optional override (sandbox mode)
    """

    demo_role = state_store.get_demo_role(user_id)

    is_demo_active = demo_role is not None

    effective_role = demo_role if is_demo_active else real_role

    return RoleContext(
        user_id=user_id,
        real_role=real_role,
        effective_role=effective_role,
        is_demo_active=is_demo_active,
    )


def get_effective_role(user_id: int, real_role: str) -> str:
    """
    Lightweight helper (for old code compatibility).
    """
    return resolve_role(user_id, real_role).effective_role