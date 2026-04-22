ROLE_HIERARCHY = {
    "R3": 1,
    "R4": 2,
    "R5": 3,
}


def can_access(
    user_role: str,
    required_role: str,
    *,
    demo_mode: bool = False,
    demo_override_role: str | None = None
) -> bool:
    """
    Access control with optional demo override.

    Rules:
    - normal mode → strict hierarchy
    - demo mode → optional role override for UI testing
    """

    # =========================
    # DEMO MODE OVERRIDE
    # =========================
    if demo_mode and demo_override_role:
        effective_role = demo_override_role
    else:
        effective_role = user_role

    # =========================
    # SAFETY GUARD
    # =========================
    if effective_role not in ROLE_HIERARCHY:
        return False

    if required_role not in ROLE_HIERARCHY:
        return False

    # =========================
    # ACCESS CHECK
    # =========================
    return ROLE_HIERARCHY[effective_role] >= ROLE_HIERARCHY[required_role]