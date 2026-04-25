# =========================================
# GROUP: services.user
# FILE: onboarding_service.py
# DESCRIPTION:
# Handles user onboarding flow (register nickname + assign role R3).
# =========================================

import logging

from src.services.user.user_profile import user_profile

logger = logging.getLogger(__name__)


class OnboardingService:
    """
    Handles first-time user onboarding.
    """

    def register_user(self, user_id: int, nick: str) -> None:
        """
        Creates or updates user profile and assigns R3 role.
        """

        profile = user_profile.get(user_id)

        # -------------------------------------------------
        # CREATE PROFILE IF NOT EXISTS
        # -------------------------------------------------
        if profile is None:
            profile = user_profile.create_or_update(
                user_id=user_id,
                nickname=nick,
            )

        # -------------------------------------------------
        # ENSURE NICK IS SET
        # -------------------------------------------------
        user_profile.set_nick(user_id, nick)

        # -------------------------------------------------
        # ASSIGN ROLE R3
        # -------------------------------------------------
        user_profile.set_role(user_id, "R3")

        logger.info(
            "Onboarding completed | user_id=%s nick=%s role=R3",
            user_id,
            nick,
        )

    def is_registered(self, user_id: int) -> bool:
        """
        Checks if user has completed onboarding.
        """

        profile = user_profile.get(user_id)

        if profile is None:
            return False

        return profile.nickname is not None


# global instance
onboarding_service = OnboardingService()