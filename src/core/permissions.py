ROLE_HIERARCHY = {
    "R3": 1,
    "R4": 2,
    "R5": 3,
}


def can_access(user_role: str, required_role: str) -> bool:
    """
    Pure permission check (production-safe).

    Rules:
    - no feature flags
    - no demo logic
    - strict hierarchy comparison
    - fails safely on invalid roles
    """

    # =========================
    # SAFETY GUARDS
    # =========================
    if user_role not in ROLE_HIERARCHY:
        return False

    if required_role not in ROLE_HIERARCHY:
        return False

    # =========================
    # ACCESS CHECK
    # =========================
    return ROLE_HIERARCHY[user_role] >= ROLE_HIERARCHY[required_role]