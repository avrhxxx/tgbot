# =========================================
# GROUP: telegram.windows.home
# FILE: home.py
# DESCRIPTION:
# UI data provider for Home screen (aiogram-dialog compatible)
# =========================================

import logging
from aiogram_dialog import DialogManager

from src.services.user.user_profile import user_profile

logger = logging.getLogger(__name__)


async def get_home_data(dialog_manager: DialogManager, **kwargs):
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

    logger.info("Rendering Home window | user_id=%s", user_id)

    return {
        "text": (
            "🏠 HOME\n\n"
            f"👤 Nick: {nickname}\n"
            f"🎮 Role: {role}"
        )
    }