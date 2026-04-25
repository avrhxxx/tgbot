# =========================================
# GROUP: telegram.windows.home
# FILE: home.py
# DESCRIPTION:
# Home screen renderer (role-aware UI).
# SINGLE SOURCE OF TRUTH = UserProfileService.
# =========================================

import logging

from src.services.user.user_profile import user_profile

logger = logging.getLogger(__name__)


def render_home(user_id: int):
    """
    Builds Home UI from live profile data.
    """

    profile = user_profile.get(user_id)

    if not profile:
        nickname = "User"
        role = "R3"
    else:
        nickname = profile.nickname or "User"
        role = profile.role

    logger.info("Rendering Home window | user=%s role=%s", user_id, role)

    text = (
        f"🏠 Home\n\n"
        f"👤 Nick: {nickname}\n"
        f"🎮 Role: {role}"
    )

    return text