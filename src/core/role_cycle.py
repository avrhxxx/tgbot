from src.ui.definitions.role_ids import RoleID


# =========================
# 🎭 ROLE CYCLE CONFIG
# =========================
ROLE_CYCLE = [
    RoleID.R3,
    RoleID.R4,
    RoleID.R5,
]


# =========================
# 🔁 GET NEXT ROLE
# =========================
def get_next_role(current_role: str) -> str:
    """
    Cycles:
    R3 -> R4 -> R5 -> R3
    """

    if current_role not in ROLE_CYCLE:
        return RoleID.R3

    idx = ROLE_CYCLE.index(current_role)
    next_idx = (idx + 1) % len(ROLE_CYCLE)

    return ROLE_CYCLE[next_idx]