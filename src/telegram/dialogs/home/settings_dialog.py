# =========================================
# GROUP: telegram.windows.home
# FILE: settings.py
# =========================================

from src.services.user.user_profile import user_profile


async def get_settings_data(dialog_manager, **kwargs):
    user_id = dialog_manager.event.from_user.id

    profile = user_profile.get(user_id)

    return {
        "text": (
            "⚙️ SETTINGS\n\n"
            f"👤 Nick: {profile.nickname if profile else 'User'}\n"
            f"🎮 Role: {profile.role if profile else 'R3'}"
        )
    }