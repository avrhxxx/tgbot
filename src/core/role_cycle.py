from src.ui.definitions.role_ids import RoleID


ROLE_CYCLE = [
    RoleID.R3,
    RoleID.R4,
    RoleID.R5,
]


def get_next_role(current_role: str) -> str:
    # normalize string → enum
    try:
        current = RoleID(current_role)
    except Exception:
        return RoleID.R3

    if current not in ROLE_CYCLE:
        return RoleID.R3

    idx = ROLE_CYCLE.index(current)
    next_idx = (idx + 1) % len(ROLE_CYCLE)

    return ROLE_CYCLE[next_idx].value