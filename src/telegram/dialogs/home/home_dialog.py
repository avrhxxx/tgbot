# =========================================
# GROUP: telegram.windows.home
# FILE: home.py
# =========================================

from src.services.user.user_profile import user_profile


async def get_home_data(dialog_manager, **kwargs):
    user_id = dialog_manager.event.from_user.id

    profile = user_profile.get(user_id)

    return {
        "text": (
            "🏠 HOME\n\n"
            f"👤 Nick: {profile.nickname if profile else 'User'}\n"
            f"🎮 Role: {profile.role if profile else 'R3'}"
        )
    }