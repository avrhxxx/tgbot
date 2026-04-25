# =========================================
# GROUP: telegram.permissions
# FILE: context.py
# DESCRIPTION:
# Unified runtime user context (STRICT TYPE SAFE)
# =========================================

from dataclasses import dataclass
from src.telegram.permissions.roles import Role


@dataclass
class UserContext:
    user_id: int
    role: Role
    nickname: str | None = None
    username: str | None = None
    first_name: str | None = None