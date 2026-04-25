# =========================================
# GROUP: telegram.windows.home
# FILE: settings.py
# =========================================

import logging

from src.services.user.user_profile import user_profile

logger = logging.getLogger(__name__)


def settings_window(user_id: int) -> dict:
    profile = user_profile.get(user_id)

    if not profile:
        return {"text": "⚙️ Settings unavailable"}

    logger.info("Rendering Settings window | user=%s", user_id)

    return {
        "text": (
            "⚙️ Settings\n\n"
            f"👤 Nick: {profile.nickname or 'User'}\n"
            f"🎮 Role: {profile.role}"
        )
    }