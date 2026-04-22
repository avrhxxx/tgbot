ROLE_HIERARCHY = {
    "R3": 1,
    "R4": 2,
    "R5": 3,
}

def can_access(user_role: str, required_role: str) -> bool:
    return ROLE_HIERARCHY[user_role] >= ROLE_HIERARCHY[required_role]