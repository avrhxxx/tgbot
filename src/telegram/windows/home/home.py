# =========================================
# GROUP: telegram.windows.home
# FILE: home.py
# =========================================

from src.services.user.user_profile import user_profile
from src.telegram.permissions.context import UserContext


async def get_home_data(dialog_manager, **kwargs):

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

    return {
        "text": (
            "🏠 HOME\n\n"
            f"👤 Nick: {nickname}\n"
            f"🎮 Role: {role}"
        )
    }