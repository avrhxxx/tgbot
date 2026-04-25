# =========================================
# GROUP: telegram.windows.home
# FILE: settings.py
# DESCRIPTION:
# SETTINGS UI window (getter only)
# =========================================

from src.services.user.user_profile import user_profile


async def get_settings_data(dialog_manager, **kwargs):
    user_id = dialog_manager.event.from_user.id

    profile = user_profile.get(user_id)

    name = (
        dialog_manager.event.from_user.username
        or dialog_manager.event.from_user.first_name
        or "User"
    )

    return {
        "text": (
            "⚙️ SETTINGS\n\n"
            f"👤 User: {name}\n"
            f"🎮 Nick: {profile.nickname if profile else '—'}\n"
            f"🎭 Role: {profile.role if profile else 'R3'}"
        )
    }