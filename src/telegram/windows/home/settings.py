# =========================================
# GROUP: telegram.windows.home
# FILE: settings.py
# DESCRIPTION:
# UI data provider for Settings screen
# =========================================

import logging
from aiogram_dialog import DialogManager

from src.services.user.user_profile import user_profile

logger = logging.getLogger(__name__)


async def get_settings_data(dialog_manager: DialogManager, **kwargs):
    user_id = dialog_manager.event.from_user.id

    profile = user_profile.get(user_id)

    nickname = (
        profile.nickname
        if profile and profile.nickname
        else dialog_manager.event.from_user.username
        or dialog_manager.event.from_user.first_name
        or "User"
    )

    role = profile.role if profile else "R3"

    logger.info("Rendering Settings window | user_id=%s", user_id)

    return {
        "text": (
            "⚙️ SETTINGS\n\n"
            f"👤 Nick: {nickname}\n"
            f"🎮 Role: {role}"
        )
    }