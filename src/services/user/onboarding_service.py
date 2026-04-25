# =========================================
# GROUP: services.user
# FILE: onboarding_service.py
# DESCRIPTION:
# Handles user onboarding flow:
# - checks if user is registered
# - saves nickname
# - assigns initial role (R3)
# =========================================

import logging

from src.services.user.user_profile import user_profile
from src.telegram.permissions.roles import Role

logger = logging.getLogger(__name__)


class OnboardingService:
    """
    Business logic for first-time user registration.
    """

    def is_registered(self, user_id: int) -> bool:
        profile = user_profile.get(user_id)
        return profile.get("game_nick") is not None

    def register_user(self, user_id: int, nick: str) -> None:
        """
        Registers user:
        - saves nickname
        - assigns R3 role
        """

        user_profile.set_nick(user_id, nick)
        user_profile.set_role(user_id, Role.R3)

        logger.info(
            "User registered | user_id=%s nick=%s role=%s",
            user_id,
            nick,
            Role.R3,
        )


onboarding_service = OnboardingService()