# =========================================
# GROUP: telegram.windows.home
# FILE: settings.py
# DESCRIPTION:
# Settings screen (role-aware, safe rendering)
# =========================================

import logging

from src.services.user.user_profile import user_profile

logger = logging.getLogger(__name__)


def render_settings(user_id: int):
    profile = user_profile.get(user_id)

    if not profile:
        return "⚙️ Settings unavailable"

    logger.info("Rendering Settings window | user=%s", user_id)

    base = (
        "⚙️ Settings\n\n"
        f"👤 Nick: {profile.nickname or 'User'}\n"
        f"🎮 Role: {profile.role}\n"
    )

    if profile.role == "R3":
        base += "\n🔒 Limited access (R3)"

    return base