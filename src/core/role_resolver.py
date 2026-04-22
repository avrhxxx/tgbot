from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class RoleContext:
    user_id: int
    real_role: str
    effective_role: str
    is_demo_active: bool


def resolve_role(user_id: int, real_role: str, demo_role: Optional[str]) -> RoleContext:
    """
    PURE FUNCTION (NO GLOBAL STATE)
    """

    is_demo_active = demo_role is not None
    effective_role = demo_role if is_demo_active else real_role

    return RoleContext(
        user_id=user_id,
        real_role=real_role,
        effective_role=effective_role,
        is_demo_active=is_demo_active,
    )


def get_effective_role(user_id: int, real_role: str, demo_role: Optional[str]) -> str:
    return resolve_role(user_id, real_role, demo_role).effective_role