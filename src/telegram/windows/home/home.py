# =========================================
# GROUP: telegram.windows.home
# FILE: home.py
# =========================================

import logging

from src.services.user.user_profile import user_profile

logger = logging.getLogger(__name__)


def home_window(user_id: int) -> dict:
    profile = user_profile.get(user_id)

    if not profile:
        nickname = "User"
        role = "R3"
    else:
        nickname = profile.nickname or "User"
        role = profile.role

    logger.info("Rendering Home window | user=%s", user_id)

    return {
        "text": (
            "🏠 Home\n\n"
            f"👤 Nick: {nickname}\n"
            f"🎮 Role: {role}"
        )
    }