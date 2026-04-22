from dataclasses import dataclass
from typing import Optional, Any


# =========================
# ROLE CONTEXT MODEL
# =========================
@dataclass(frozen=True)
class RoleContext:
    user_id: int
    real_role: str
    effective_role: str
    is_demo_active: bool


# =========================
# ROLE RESOLVER (SOURCE OF TRUTH)
# =========================
def resolve_role(state: Any) -> RoleContext:
    """
    SINGLE SOURCE OF TRUTH FOR ROLE RESOLUTION

    - real_role = role zapisany w state
    - demo_role = optional override (if exists in state)
    - effective_role = final role used in UI
    """

    user_id = getattr(state, "user_id", None)
    real_role = getattr(state, "role", None)

    # optional override (safe fallback)
    demo_role = getattr(state, "demo_role", None)

    is_demo_active = demo_role is not None
    effective_role = demo_role if is_demo_active else real_role

    return RoleContext(
        user_id=user_id,
        real_role=real_role,
        effective_role=effective_role,
        is_demo_active=is_demo_active,
    )