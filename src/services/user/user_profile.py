# =========================================
# GROUP: services.user
# FILE: user_profile.py
# DESCRIPTION:
# In-memory user profile storage (MVP layer).
# Will later be replaced by DB (PostgreSQL / Redis).
# =========================================

import logging
from dataclasses import dataclass
from typing import Dict

logger = logging.getLogger(__name__)


@dataclass
class UserProfile:
    user_id: int
    nickname: str | None = None
    role: str = "R3"


class UserProfileService:
    """
    Simple in-memory profile storage.
    Replace later with DB layer.
    """

    def __init__(self):
        self._storage: Dict[int, UserProfile] = {}
        logger.info("UserProfileService initialized")

    def get(self, user_id: int) -> UserProfile | None:
        return self._storage.get(user_id)

    def create_or_update(self, user_id: int, nickname: str) -> UserProfile:
        profile = self._storage.get(user_id)

        if profile:
            profile.nickname = nickname
        else:
            profile = UserProfile(
                user_id=user_id,
                nickname=nickname,
                role="R3",
            )
            self._storage[user_id] = profile

        logger.info(
            "UserProfile saved | user_id=%s nickname=%s",
            user_id,
            nickname,
        )

        return profile

    # =========================================
    # 🔥 COMPAT LAYER (fix for onboarding)
    # =========================================

    def set_nick(self, user_id: int, nick: str) -> UserProfile:
        profile = self._storage.get(user_id)

        if not profile:
            profile = UserProfile(user_id=user_id, nickname=nick, role="R3")
            self._storage[user_id] = profile
        else:
            profile.nickname = nick

        logger.info("Nick updated | user_id=%s nick=%s", user_id, nick)
        return profile

    def set_role(self, user_id: int, role: str) -> UserProfile:
        profile = self._storage.get(user_id)

        if not profile:
            profile = UserProfile(user_id=user_id, role=role)
            self._storage[user_id] = profile
        else:
            profile.role = role

        logger.info("Role updated | user_id=%s role=%s", user_id, role)
        return profile


# global instance
user_profile = UserProfileService()